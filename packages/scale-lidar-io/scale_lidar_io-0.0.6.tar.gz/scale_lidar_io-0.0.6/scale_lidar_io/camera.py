import cv2
import numpy as np
from PIL import Image, ImageDraw

from .color_utils import map_colors
from .transform import Transform


class LidarCamera:
    world2cam = Transform.from_euler([-90, 0, -90], degrees=True)

    def __init__(self, camera_id):
        self.id = camera_id
        self.pose = Transform(self.world2cam)
        self.K = np.eye(3, dtype=np.float32)
        self.D = np.zeros(5, dtype=np.float32)
        self.model = None

    @property
    def position(self) -> np.ndarray:
        return self.pose.position

    @property
    def rotation(self) -> np.ndarray:
        return self.pose.rotation

    @property
    def world_transform(self) -> Transform:
        return self.pose @ self.world2cam.T

    @property
    def fx(self):
        return self.K[0, 0]

    @property
    def fy(self):
        return self.K[1, 1]

    @property
    def cx(self):
        return self.K[0, 2]

    @property
    def cy(self):
        return self.K[1, 2]

    @property
    def extrinsic_matrix(self):
        return self.pose.inverse[:3, :4]

    @property
    def projection_matrix(self):
        return self.K @ self.extrinsic_matrix

    @position.setter
    def position(self, position: np.ndarray):
        self.pose.position = position

    @rotation.setter
    def rotation(self, rotation):
        self.pose.rotation = Transform(rotation).rotation

    @world_transform.setter
    def world_transform(self, transform: Transform):
        self.pose = transform @ self.world2cam

    @extrinsic_matrix.setter
    def extrinsic_matrix(self, matrix):
        self.pose = Transform(matrix).inverse

    @projection_matrix.setter
    def projection_matrix(self, P):
        assert P.shape == (3, 4), 'Projection matrix should be 3x4'
        K, R, t, _, _, _, _ = cv2.decomposeProjectionMatrix(P)
        self.pose = Transform.from_Rt(R.T, t[:3, 0] / t[3, 0])
        self.K = K

    def calibrate(self, position=None, rotation=None, pose=None, extrinsic_matrix=None, projection_matrix=None, K=None, D=None, model=None, **kwargs):
        """
        Helper for camera calibration
        :param position: Camera position [x, y, z]
        :param rotation: Camera rotation/heading
        :param pose: Camera pose (position + rotation)
        :param extrinsic_matrix: extrinsic 4x4 matrix (world to camera transform)
        :param projection_matrix: 3x4 projection matrix
        :param K: intrinsic 3x3 matrix
        :param D: distortion values
        :param model: camera model
        """
        if position is not None:
            self.position = position
        if rotation is not None:
            self.rotation = rotation
        if pose is not None:
            self.pose = Transform(pose)
        if extrinsic_matrix is not None:
            self.extrinsic_matrix = extrinsic_matrix
        if projection_matrix is not None:
            self.projection_matrix = projection_matrix
        if K is not None:
            self.K = np.array(K[:3, :3])
        if D is not None:
            self.D = D
        if model is not None:
            self.model = model
        if 'world_transform' in kwargs:
            self.world_transform = kwargs['world_transform']
        if 'fx' in kwargs:
            self.K[0, 0] = kwargs['fx']
        if 'fy' in kwargs:
            self.K[1, 1] = kwargs['fy']
        if 'cx' in kwargs:
            self.K[0, 2] = kwargs['cx']
        if 'cy' in kwargs:
            self.K[1, 2] = kwargs['cy']

    def apply_transform(self, transform: Transform):
        self.pose = transform @ self.pose

    def rotate(self, angles, degrees=True):
        self.apply_transform(Transform.from_euler(angles, degrees=degrees))

    def translate(self, vector):
        self.apply_transform(Transform(vector))

    def project_points(self, points: np.ndarray, use_distortion=False):
        if self.model == 'cylindrical':
            cx = self.K[0][2]
            cy = self.K[1][2]
            fx = self.K[0][0]
            fy = self.K[1][1]
            projected = Transform(self.extrinsic_matrix) @ points[:, :3]
            theta = np.arctan2(projected[:, 0], projected[:, 2])
            r = np.hypot(projected[:, 0], projected[:, 2])
            u = theta * fx + cx
            v = projected[:, 1] / r * fy + cy
            projected[:, 0] = u
            projected[:, 1] = v
            projected[:, 2] = 1
        else:
            projected = Transform(self.projection_matrix) @ points[:, :3]

            # projected = ((points[:, :3] - self.position) @ self.rotation) @ self.intrinsic_matrix[:3, :3].T
            projected[:, 0] /= np.where(projected[:, 2] == 0, np.inf, projected[:, 2])
            projected[:, 1] /= np.where(projected[:, 2] == 0, np.inf, projected[:, 2])

        if use_distortion:
            projected[:, :2] = cv2.projectPoints(
                objectPoints=np.array(points[:, :3]),
                rvec=cv2.Rodrigues(self.extrinsic_matrix[:3, :3])[0],
                tvec=self.extrinsic_matrix[:3, 3],
                distCoeffs=self.D,
                cameraMatrix=self.K,
            )[0].reshape((-1, 2))

        return np.hstack([
            projected[:, :3],
            points[:, 3:]
        ])

    def get_projected_image(self, image, points, frame_transform, color_mode='default'):
        assert image, 'No image loaded.'
        def crop_points(points, bounding_box):
            conditions = np.logical_and(points[:, :3] >= bounding_box[0], points[:, :3] < bounding_box[1])
            mask = np.all(conditions, axis=1)
            return points[mask]
        im = image.get_image().convert('RGBA')
        radius = 3
        oversample = 3
        # Project points image
        points_im = Image.new('RGBA', (im.size[0] * oversample, im.size[1] * oversample))

        draw = ImageDraw.Draw(points_im)

        projected = self.project_points(points, use_distortion=False)
        projected = crop_points(projected,
                                np.array([[0, 0, 0.1], [im.size[0], im.size[1], np.inf]]))

        # Returns original image if not projected points on image
        if not len(projected):
            return im

        colors = map_colors(projected, color_mode)

        for point, color in zip(projected[:, :2] * oversample, colors):
            draw.ellipse([tuple(point - radius), tuple(point + radius)], fill=tuple(color))
        points_im = points_im.resize(im.size, Image.CUBIC)

        # Merge images
        projected_im = Image.composite(points_im, im, points_im)
        return projected_im

    def __repr__(self):
        return 'LidarCamera({0}) {1}'.format(self.id, self.pose)
