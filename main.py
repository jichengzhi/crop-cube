import os.path

from stl import mesh

from align import best_degree_for_rotation_bisearch
from clean import clean
from diff import get_upper_cube, degrees_to_face_y
from display import plot_3d
from rotate import rotate_z


def load_points_from_stl(stl_filename: str):
    m = mesh.Mesh.from_file(stl_filename)
    return m.vectors.reshape(-1, 3)


def cube_name_from_filename(stl_filename: str):
    basename = os.path.basename(stl_filename)
    return basename.split('.')[0]


if __name__ == '__main__':
    stl_path = 'Blue09.STL'

    raw_data = load_points_from_stl(stl_path)
    cube = clean(raw_data)  # only keep cube points
    d = best_degree_for_rotation_bisearch(cube)
    aligned_cube = rotate_z(cube, d)  # cube is aligned to axis
    upper = get_upper_cube(aligned_cube)  # get upper part of the cube for pattern matching
    final_cube = rotate_z(aligned_cube, degrees_to_face_y(upper) - 90)  # X is facing us

    cube_name = cube_name_from_filename(stl_path)
    cube_path = os.path.join('./output', f'cube-{cube_name}.png')
    plot_3d(final_cube, title=f'cube from {stl_path}', path=cube_path, s=0.1)
