import numpy as np

X, Y, Z = 0, 1, 2


def sample_target_surface(cube_points, h=0.5):
    """
    Sample the target surface: the face at top when X is facing us.
    
    :param h: height of the surface
    :param cube_points: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :return: a 3D array of points on target surface
    """
    max_z = max(cube_points[:, Z])

    def within_surface(z):
        return max_z - z <= h

    return np.array([pt for pt in cube_points if within_surface(pt[Z])])
