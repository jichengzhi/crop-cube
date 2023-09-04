from pathlib import Path

from stl import mesh


def load_points_from_stl(stl_path: Path):
    m = mesh.Mesh.from_file(str(stl_path))
    return m.vectors.reshape(-1, 3)


def cube_name_from_stl_path(stl_path: Path):
    return stl_path.stem
