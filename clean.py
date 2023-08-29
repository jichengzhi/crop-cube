import numpy as np

X, Y, Z = 0, 1, 2


def __key(xyz):
    x, y, _ = xyz
    return round(x, 2), round(y, 2)


def __max_h_by_xy(points):
    table = {}

    for pt in points:
        x, y, z = pt

        key = __key(pt)

        if key not in table:
            table[key] = z
        else:
            table[key] = max(table[key], z)

    return table


def clean(points):
    """
    Filter out points that are not within the cube.

    Note: this function also filters some points within the cube!
    :param points: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :return: points within the cube
    """
    z_table = __max_h_by_xy(points)

    max_z = max(points[:, Z])

    def within_cube(pt):
        z = z_table[__key(pt)]
        return max_z - z < 10

    return np.array([pt for pt in points if within_cube(pt)])
