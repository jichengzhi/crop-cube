import numpy as np

from rotate import rotate_z

X, Y, Z = 0, 1, 2


def get_upper_cube(cube_points):
    """
    Get upper part of the cube.

    Why? We need to distinguish the four faces in order to rotate the "X face" to us.
    By looking at upper part of all faces, we can see that there's an empty "V" on the "X face"
    and an empty "I" on the "Y face".

    Since detecting empty "I" is easier than detecting empty "V", we can find the "Y face" first
    and then rotate a fixed degree to reach the "X face".

    :param cube_points: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :return: 3D points of the cube's upper part
    """
    max_z = max(cube_points[:, Z])

    def within_upper(pt):
        return max_z - pt[Z] <= 10  # better to use percentage of height

    return np.array([pt for pt in cube_points if within_upper(pt)])


def get_closest_face(cube_points):
    """
    Detect the surface that is the closest one to us and return its 2D representation.

    :param cube_points: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :return: a 2D array (xyz -> xz) of points on the surface
    """
    min_y = min(cube_points[:, Y])

    def close_enough(pt):
        return abs(pt[Y] - min_y) < 3  # better to use percentage of width

    xyz = np.array([pt for pt in cube_points if close_enough(pt)])
    return xyz[:, [X, Z]]


def face_to_grid(xy, row=50, col=50):
    """
    Convert the face to a grid. By doing so we discard useless details
    and can focus on recognize patterns.

    :param xy: a 2D numpy array, whose elements are [x, y]
    :param row: number of cells in each row
    :param col: number of cells in each column
    :return: a 2D array with shape (row, col)
    """
    xs = xy[:, X]
    ys = xy[:, Y]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # print(f'x: [{min_x}, {max_x}], y: [{min_y}, {max_y}]')

    x_range = (max_x - min_x) / col
    y_range = (max_y - min_y) / row

    # print(f'x range: {x_range}, y range: {y_range}')

    grid = np.zeros((row, col))

    for x, y in xy:
        c = int((x - min_x) // x_range)
        r = int((y - min_y) // y_range)

        if r == row:
            r -= 1
        if c == col:
            c -= 1

        try:
            grid[r][c] = 1
        except IndexError:
            print(f'({x}, {y}) -> ({r}, {c})')
            return None

    return grid[::-1]


def degrees_to_face_y(top_cube, row=30, col=30, min_pattern_len=10):
    """
    Find out degree for rotation to bring face Y facing us.

    :param top_cube: a 3D array of [x, y, z]
    :param row: number of cells in each row
    :param col: number of cols in each row
    :param min_pattern_len: minimum number of grids composing the empty "I"
    :return: degree to rotate
    """
    for i in range(4):
        xyz = rotate_z(top_cube, i * 90)
        xy = get_closest_face(xyz)

        grid = face_to_grid(xy, row=row, col=col)

        for c in range(col):

            r = row - 1

            if grid[r][c] == 1:
                continue

            while r >= 0 and grid[r][c] == 0:
                r -= 1

            n = row - 1 - r

            if n >= min_pattern_len:
                return i * 90
    raise RuntimeError('cannot find degree to face Y')
