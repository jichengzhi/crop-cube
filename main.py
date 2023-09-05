from pathlib import Path

import matplotlib.pyplot as plt

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


if __name__ == '__main__':

    work_dir = Path('.')
    # sample_dir_name = 'Printer3samples'

    for sample_dir_name in ['Printer1samples', 'Printer5samples']:

        work_dir = Path('C:\Data', sample_dir_name)
        stl_paths = list(work_dir.glob('**/*.STL'))

        for stl_path in stl_paths:
            print(f'working on stl file from {stl_path.absolute()}')

            raw_data = load_points_from_stl(stl_path)
            cube_name = cube_name_from_stl_path(stl_path)

            cube, sample_points = sample_from_raw_points(raw_data)

            output_dir = Path(sample_dir_name)
            output_dir.mkdir(parents=True, exist_ok=True)

            cube_img_path = str(Path(output_dir, f'cube-{cube_name}.png'))
            surface_img_path = str(Path(output_dir, f'surface-{cube_name}.png'))
            heatmap_img_path = str(Path(output_dir, f'heatmap-{cube_name}.png'))

            export_sample_in_2d(sample_points, cube_name, surface_img_path)

            plot_3d(cube, title=f'cube from {stl_path}', path=cube_img_path, s=0.1)

            heatmap = get_heatmap(sample_points)
            plot_heatmap(heatmap, cube_name=cube_name, save_path=heatmap_img_path)
