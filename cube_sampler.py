from align import best_degree_for_rotation_bisearch
from clean import clean
from diff import get_upper_cube, degrees_to_face_y
from rotate import rotate_z
from sample import sample_target_surface


def sample_from_raw_points(raw_data):
    cube = clean(raw_data)  # only keep cube points
    d = best_degree_for_rotation_bisearch(cube)
    aligned_cube = rotate_z(cube, d)  # cube is aligned to axis
    upper = get_upper_cube(aligned_cube)  # get upper part of the cube for pattern matching
    final_cube = rotate_z(aligned_cube, degrees_to_face_y(upper) - 90)  # X is facing us
    sample = sample_target_surface(final_cube)

    return final_cube, sample
