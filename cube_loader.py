import os

from stl import mesh


def load_points_from_stl(stl_path: str):
    m = mesh.Mesh.from_file(stl_path)
    return m.vectors.reshape(-1, 3)


def cube_name_from_stl_path(stl_path: str):
    basename = os.path.basename(stl_path)
    return basename.split('.')[0]
