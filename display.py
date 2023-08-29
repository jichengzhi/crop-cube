import matplotlib.pyplot as plt

from diff import get_closest_face, face_to_grid
from rotate import rotate_z

X, Y, Z = 0, 1, 2


def plot_cube_around_z(xyz, s=0.00001):
    """
    Rotate the cube around z-axis and plot all faces.
    :param xyz: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :param s: size of each point, see param s in doc of matplotlib.pyplot.scatter
    :return: None
    """
    fig = plt.figure(figsize=plt.figaspect(0.5))
    fig.tight_layout()

    for i in range(4):
        degree = i * 90
        data = rotate_z(xyz, degree)

        ax = fig.add_subplot(2, 2, i + 1, projection='3d')
        ax.scatter(data[:, X], data[:, Y], data[:, Z], s=s)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'rotate_z({degree})', fontsize=10, y=1.0)

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def plot_3d(xyz, title='', s=0.00001):
    """
    Plot coordinates in 3D.
    :param xyz: a numpy array with shape (n, 3), whose elements are coordinates in format [x, y, z]
    :param title: title of the graph
    :param s: size of each point, see param s in doc of matplotlib.pyplot.scatter
    :return: None
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(xyz[:, X], xyz[:, Y], xyz[:, Z], s=s)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title, fontsize=10, y=1.0)

    plt.show()


def plot_grid(xy):
    fig, ax = plt.subplots()
    ax.imshow(xy)
    plt.show()


def plot_grids(upper_cube, row=30, col=30):
    fig, ax = plt.subplots(2, 2)

    for i in range(4):
        r = int(i // 2)
        c = i % 2

        xyz = rotate_z(upper_cube, i * 90)
        face = get_closest_face(xyz)
        grid = face_to_grid(face, row=row, col=col)
        ax[r, c].imshow(grid)

    plt.show()
