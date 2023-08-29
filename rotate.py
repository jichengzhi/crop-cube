import math

import numpy as np


def rotate_z(xyz, degree: float):
    """
    Rotate points around z-axis.
    :param xyz: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :param degree: degrees to rotate
    :return: coordinate of points after rotation
    """
    r = math.radians(degree)

    rotation_matrix = np.array([
        [np.cos(r), -np.sin(r), 0],
        [np.sin(r), np.cos(r), 0],
        [0, 0, 1]
    ])

    return xyz.dot(rotation_matrix.T)


def rotate_x(xyz, degree: float):
    """
    Rotate points around x-axis.
    :param xyz: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :param degree: degrees to rotate
    :return: coordinate of points after rotation
    """
    r = math.radians(degree)

    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(r), -np.sin(r)],
        [0, np.sin(r), np.cos(r)]
    ])

    return xyz.dot(rotation_matrix.T)
