from rotate import rotate_z

X, Y, Z = 0, 1, 2


def closest_points_count(points):
    min_y = min(points[:, Y])

    def is_min(pt):
        return abs(pt[Y] - min_y) <= 1

    return len([pt for pt in points if is_min(pt)])


def best_degree_for_rotation(points):
    """
    Find the degree for rotation to align the cube to axis.

    This is the brute force approach, iterating all degrees and pick the best.
    After alignment, points of one face should be found at minimum y of all points.
    :param points: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :return: the best degree
    """
    best_count = 0
    best_degree = 0

    for d in range(90):
        rotated = rotate_z(points, d)

        n = closest_points_count(rotated)

        print(f'd={d}, n={n}')

        if n > best_count:
            best_count = n
            best_degree = d

    return best_degree


def best_degree_for_rotation_bisearch(points):
    """
    Find the degree for rotation to align the cube to axis.

    This is the binary search approach.

    The degree for rotation is in range [0, 90). If we plot `f(degree) = closest_points_count(degree)`
    with domain [0, 90), we can find only one peak value on the graph, which is the
    best degree.

    So we can divide degrees into two parts:

    - degrees below the best one => `f(degree)` < `f(a greater degree)` for these degrees
    - the best degree and greater ones => `f(degree)` > `f(a greater degree)` for these degrees

    :param points: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :return: the best degree
    """
    l, r = 0, 90
    mid = 0

    while r - l > 0.01:
        mid = (l + r) / 2

        n = closest_points_count(rotate_z(points, mid))
        rt = closest_points_count(rotate_z(points, mid + 2))
        lf = closest_points_count(rotate_z(points, mid - 2))

        # print(mid, lf, n, rt)

        if n > rt and n > lf:
            return mid
        elif rt < n < lf:
            r = mid
        else:
            l = mid + 0.1

    return mid
