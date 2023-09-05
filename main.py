import os
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
from dotenv import load_dotenv

from cube_loader import cube_name_from_stl_path, load_points_from_stl
from cube_sampler import sample_from_raw_points
from display import plot_3d
from heatmap import plot_heatmap, get_heatmap
from rotate import rotate_x


def export_sample_in_2d(sample_points, cube_name, img_path: str):
    X, Y, Z = 0, 1, 2
    surface = rotate_x(sample_points, -90)[:, [X, Z]]

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(surface[:, 0], surface[:, 1], s=0.001)
    ax.set_title(f'{cube_name} surface', fontsize=10, y=1.0)
    plt.savefig(img_path)


def printer_dirs(sample_root: Path) -> List[Path]:
    return [Path(sample_root, dir_name) for dir_name in os.getenv('PRINTER_FOLDERS').split(',')]


if __name__ == '__main__':

    load_dotenv('.env.local')

    sample_root = Path(os.getenv('SAMPLE_ROOT'))
    output_root = Path(os.getenv('OUTPUT_ROOT'))

    for printer_dir in printer_dirs(sample_root):

        stl_paths = list(printer_dir.glob('**/*.STL'))

        for stl_path in stl_paths:
            print(f'Processing {stl_path.absolute()}')

            raw_data = load_points_from_stl(stl_path)
            cube_name = cube_name_from_stl_path(stl_path)

            cube, sample_points = sample_from_raw_points(raw_data)

            output_dir = Path(output_root, printer_dir.name)
            output_dir.mkdir(parents=True, exist_ok=True)

            cube_img_path = str(Path(output_dir, f'cube-{cube_name}.png'))
            surface_img_path = str(Path(output_dir, f'surface-{cube_name}.png'))
            heatmap_img_path = str(Path(output_dir, f'heatmap-{cube_name}.png'))

            export_sample_in_2d(sample_points, cube_name, surface_img_path)

            plot_3d(cube, title=f'cube from {stl_path}', path=cube_img_path, s=0.1)

            heatmap = get_heatmap(sample_points)
            plot_heatmap(heatmap, cube_name=cube_name, save_path=heatmap_img_path)
