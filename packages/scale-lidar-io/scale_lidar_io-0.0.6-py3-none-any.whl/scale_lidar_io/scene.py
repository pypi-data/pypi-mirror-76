import hashlib
import os
import shutil
import tempfile
import zipfile
from concurrent import futures
from io import BytesIO
from typing import Any, MutableMapping, List, Dict

import boto3
import numpy as np
import pandas as pd
import ujson
from PIL import Image, ImageEnhance
from scaleapi import Task

from .camera import LidarCamera
from .transform import Transform

UPLOAD_POOL_SIZE = 8
s3 = boto3.client('s3')


def format_lidar_point(p):
    return dict(zip(('x', 'y', 'z', 'i', 'd'), p))


def format_point(p):
    return dict(zip(('x', 'y', 'z'), p))


def format_quaternion(q):
    return dict(zip(['w', 'x', 'y', 'z'], q))


def fp_md5(fp: BytesIO):
    fp.seek(0)
    md5 = hashlib.md5()
    buf = fp.read(2 ** 20)
    while buf:
        md5.update(buf)
        buf = fp.read(2 ** 20)
    fp.seek(0)
    return md5.hexdigest()


def get_s3_etag(bucket, key):
    try:
        return s3.head_object(Bucket=bucket, Key=key)['ETag'].strip('"')
    except Exception:
        pass


def s3_smart_upload(bucket, key, fileobj, content_type):
    s3_hash = get_s3_etag(bucket, key)
    local_hash = fp_md5(fileobj)

    if s3_hash == local_hash:
        print(f'File exists: {bucket}/{key}')
        return

    print(f'Uploading {bucket}/{key}...')
    s3.upload_fileobj(
        Fileobj=fileobj,
        Bucket=bucket,
        Key=key,
        ExtraArgs={'ContentType': content_type}
    )


class LidarImage:
    """LidarImage objects are represent an image and LidarCamera reference."""

    def __init__(self, camera):
        self.camera = camera
        self.file = None
        self.transform = None
        self.metadata = None

    def load_file(self, file):
        if not isinstance(file, str):
            print('WARNING: No file!')
        self.file = file

    def load_pil_image(self, pil_image: Image.Image):
        self.file = tempfile.mktemp(suffix='jpg')
        pil_image.save(self.file, format='JPEG', quality=70, optimize=True)
        print(f'Temp file created: {self.file}')

    # Legacy method
    def load(self, image):
        print('DEPRECATED METHOD LidarImage.load(), please use .load_file() or .load_pil_image()')
        if isinstance(image, Image.Image):
            self.load_pil_image(image)
        else:
            self.load_file(image)

    def get_file(self):
        return self.file

    def get_image(self):
        return Image.open(self.file)

    def scale(self, scale_factor):
        im = self.get_image()
        size = (int(im.width * scale_factor), int(im.height * scale_factor))
        self.load_pil_image(im.resize(size, Image.LANCZOS))

    def as_array(self):
        return np.asarray(self.get_image())

    def set_brightness(self, factor):
        im = ImageEnhance.Brightness(self.get_image()).enhance(factor)
        self.load_pil_image(im)

    def save(self, target_file):
        shutil.copyfile(self.file, target_file)

    def s3_upload(self, bucket, key):
        with open(self.get_file(), 'rb') as fp:
            s3_smart_upload(
                bucket=bucket,
                key=key,
                fileobj=fp,
                content_type='image/jpeg'
            )


class LidarFrame:
    """Frame objects represent all the point cloud, image, and other data that is sent to the annotator."""

    def __init__(self, frame_id, cameras):
        self.id = frame_id
        self.cameras: pd.Series[Any, LidarCamera] = cameras
        self.images: pd.Series[Any, LidarImage] = pd.Series(dtype=object)
        self.points: np.ndarray = np.zeros((0, 5), dtype=float)
        self.transform = Transform()

    def get_image(self, camera_id) -> LidarImage:
        """
        Get a image by camera_id and creates one if not exists
        :param camera_id: The camera id
        :return: LidarImage
        """
        assert camera_id in self.cameras, 'Camera not found'
        if camera_id not in self.images:
            if isinstance(camera_id, int):
                self.images.index = self.images.index.astype(int)
            self.images[camera_id] = LidarImage(camera=self.cameras[camera_id])
        return self.images[camera_id]

    def add_points(self, points: np.array, transform: Transform = None, intensity=1, sensor_id=0):
        if points.ndim == 1:
            points = np.array([points])
        if points.shape[1] == 3:
            points = np.hstack([points, np.ones((points.shape[0], 1)) * intensity])
        if transform is not None:
            points = transform.apply(points)

        points = np.hstack([points, np.ones((points.shape[0], 1)) * sensor_id])

        self.points = np.vstack([self.points, points])

    def add_debug_lines(self, intensity=1, length=5, device=0):
        x_line = np.array([np.array([length * k / 100, 0, 0]) for k in range(0, 100)])
        for camera in self.cameras:
            self.add_points(x_line, transform=camera.world_transform, intensity=intensity)

    def get_world_points(self):
        return np.hstack([self.transform @ self.points[:, :3], self.points[:, 3:4], self.points[:, 4:5]])

    def get_projected_image(self, camera_id, color_mode='default', **kwargs):
        return self.cameras[camera_id].get_projected_image(self.get_image(camera_id), self.points, self.transform,
                                                           color_mode, **kwargs)

    def get_filename(self):
        return "frame-%s.json" % self.id

    def apply_transform(self, T):
        self.transform = Transform(T) @ self.transform

    def filter_points(self, min_intensity=None, min_intensity_percentile=None):
        if min_intensity is not None:
            self.points = self.points[self.points[:, 3] >= min_intensity]
        if min_intensity_percentile is not None:
            self.points = self.points[self.points[:, 3] >= np.percentile(self.points[:, 3], min_intensity_percentile)]

    def to_json(self, public_url=''):

        def format_image(camera):
            image = self.images[camera.id]
            wct = (image.transform or self.transform) @ camera.pose
            result = dict(
                position=format_point(wct.position),
                heading=format_quaternion(wct.quaternion),
                image_url='%s/image-%s-%s.jpg' % (public_url, camera.id, self.id),
                camera_model=camera.model,
                fx=camera.fx,
                fy=camera.fy,
                cx=camera.cx,
                cy=camera.cy,
                k1=float(camera.D[0]),
                k2=float(camera.D[1]),
                p1=float(camera.D[2]),
                p2=float(camera.D[3]),
                k3=float(camera.D[4]),
            )
            if image.metadata:
                result['metadata'] = image.metadata
            return result

        images_json = self.cameras[self.images.index].apply(format_image).to_json(orient='records')
        points_json = pd.DataFrame(self.get_world_points(), columns=['x', 'y', 'z', 'i', 'd']) \
            .to_json(double_precision=4, orient='records', date_format=None)

        out = ujson.dumps({
            'images': "__IMAGES__",
            'points': "__POINTS__",
            'device_position': format_point(self.transform.position),
            'device_heading': format_quaternion(self.transform.quaternion)
        })

        out = out.replace('"__IMAGES__"', images_json)
        out = out.replace('"__POINTS__"', points_json)

        return out

    def save(self, path, public_url=''):
        # Save frame
        with open(os.path.join(path, 'frame-%s.json' % self.id), 'w') as file:
            file.write(self.to_json(public_url))

        # Save images
        for camera_id, image in self.images.items():
            image.save(os.path.join(path, 'image-%s-%s.jpg' % (camera_id, self.id)))

    def s3_upload(self, bucket, path):
        # print(f'Uploading frame {self.id}...')
        public_url = f"s3://{bucket}/{path}"

        # Upload frame json file
        s3_smart_upload(
            fileobj=BytesIO(bytes(self.to_json(public_url), encoding='utf-8')),
            bucket=bucket,
            key=f'{path}/frame-{self.id}.json',
            content_type='application/json'
        )

        # Upload images
        for camera_id, image in self.images.items():
            image.s3_upload(bucket, f'{path}/image-{camera_id}-{self.id}.jpg')

    def __repr__(self):
        return 'Frame({0}) {1}'.format(self.id, self.transform)


class LidarScene:
    """LidarScene object represent all frames on a scene."""

    def __init__(self):
        """

        :rtype: object
        """
        self.cameras: MutableMapping[LidarCamera] = pd.Series()
        self.frames: MutableMapping[LidarFrame] = pd.Series()
        self.public_url = None

    def get_camera(self, camera_id=None, index=None) -> LidarCamera:
        """
        Get a camera by id (or index) and creates one if not exists
        :param index: The camera index
        :param camera_id: The camera id
        :return: LidarCamera
        """
        assert camera_id is not None or index is not None, 'id or index must be specified'

        if camera_id is None:
            camera_id = self.cameras.index[index]

        if camera_id not in self.cameras:
            if isinstance(camera_id, int):
                self.cameras.index = self.cameras.index.astype(int)
            self.cameras[camera_id] = LidarCamera(camera_id)
        return self.cameras[camera_id]

    def get_frame(self, frame_id=None, index=None) -> LidarFrame:
        """
        Get a frame by id (or index) and creates one if not exists
        :param index: The frame index
        :param frame_id: The frame id
        :return: LidarFrame
        """
        assert frame_id is not None or index is not None, 'id or index must be specified'

        if frame_id is None:
            frame_id = self.frames.index[index]

        if frame_id not in self.frames:
            if isinstance(frame_id, int):
                self.frames.index = self.frames.index.astype(int)
            self.frames[frame_id] = LidarFrame(frame_id, cameras=self.cameras)
        return self.frames[frame_id]

    def apply_transforms(self, world_transforms: List[Transform]):
        for idx in range(len(self.frames)):
            self.get_frame(index=idx).apply_transform(world_transforms[idx])

    def filter_points(self, min_intensity=None, min_intensity_percentile=None):
        for frame in self.frames:
            frame.filter_points(min_intensity, min_intensity_percentile)

    def apply_transform(self, world_transform: Transform):
        for idx in range(len(self.frames)):
            self.get_frame(index=idx).apply_transform(world_transform)

    def make_transforms_relative(self):
        offset = self.get_frame(index=0).transform.inverse
        for frame in self.frames:
            frame.transform = offset @ frame.transform

    def to_dict(self, public_url=None):
        if public_url is None:
            public_url = self.public_url
        return dict(frames=['%s/frame-%s.json' % (public_url, frame.id) for frame in self.frames])

    def s3_upload(self, bucket, path=None, mock_upload=False, use_threads=True):
        self.public_url = f"s3://{bucket}/{path}"

        print('Uploading scene to S3: %s' % self.public_url)
        scene_dict = self.to_dict(self.public_url)

        poses_csv = pd.DataFrame(self.frames.map(lambda f: list(f.transform.matrix.reshape(-1))).to_dict()).T.to_csv(
            header=False)

        if not mock_upload:
            # Upload scene json file
            s3_smart_upload(
                bucket=bucket,
                key=f'{path}/scene.json',
                fileobj=BytesIO(bytes(ujson.dumps(scene_dict), encoding='utf-8')),
                content_type='application/json'
            )

            # Upload ego2world csv file
            s3_smart_upload(
                bucket=bucket,
                key=f'{path}/ego2world.csv',
                fileobj=BytesIO(bytes(poses_csv, encoding='utf-8')),
                content_type='text/plain'
            )

            if use_threads:
                with futures.ThreadPoolExecutor(max_workers=UPLOAD_POOL_SIZE) as executor:
                    future_list = [
                        executor.submit(LidarFrame.s3_upload, frame, bucket, path)
                        for frame in self.frames
                    ]

                    for future in future_list:
                        future.result()

            else:
                for frame in self.frames:
                    frame.s3_upload(bucket, path)

        signed_url = s3.generate_presigned_url('get_object', Params={
            'Bucket': bucket,
            'Key': f'{path}/scene.json'
        })

        print(f'Scene uploaded: {signed_url}')
        return self.public_url

    def save_task(self, filepath, template=None):
        print('Saving scene:', filepath)
        with zipfile.ZipFile(filepath, mode='w') as out:
            # Save task
            scene_dict = self.to_dict('')
            task_dict = dict(
                template or {},
                attachment_type='json',
                attachments=scene_dict['frames']
            )
            out.writestr('task.json', ujson.dumps(task_dict))

            # Save frames
            for frame in self.frames:
                # Save points
                data = frame.to_json('')
                out.writestr('frame-%s.json' % frame.id, data, compress_type=zipfile.ZIP_DEFLATED)

                # Save frame images
                for camera_id, image in frame.images.items():
                    if not image.file:
                        assert NotImplemented('Only file-imported Images supported')
                    out.write(image.file, 'image-%s-%s.jpg' % (camera_id, frame.id))
        print('Scene saved.')

    def create_task(self, template: Dict = None, task_type: str = 'lidarannotation') -> Task:
        """ Creates a Scale platform task from the configured scene

        Args:
            template: Dictionary of payload for task creation
            task_type: Select a Scale API endpoint top upload data to, currently supports 'lidarannotation' and 'lidartopdown'. Defaults to 'lidarannotation'.

        Returns:
            Task object with related information. Inherited from `scaleapi.Task` object.
        """
        if task_type == 'lidarannotation':
            from .task import LidarAnnotationTask
            return LidarAnnotationTask.from_scene(self, template)
        elif task_type == 'lidartopdown':
            from .task import LidarTopDownTask
            return LidarTopDownTask.from_scene(self, template)
        else:
            assert NotImplemented(f'Specified task_type {task_type} is not supported')
