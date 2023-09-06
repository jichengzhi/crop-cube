import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from joblib import Parallel, delayed

from cube_loader import cube_name_from_stl_path, load_points_from_stl
from cube_sampler import sample_from_raw_points
from display import plot_3d, export_sample_in_2d
from heatmap import plot_heatmap, sample_to_heatmap


def printer_dirs(sample_root: Path) -> List[Path]:
    return [Path(sample_root, dir_name) for dir_name in os.getenv('PRINTER_FOLDERS').split(',')]


def process_stl(stl_path: Path, printer_dir: Path) -> str:
    if 'test' in stl_path.stem:
        print(f'Skip test file {stl_path.absolute()}')
        return 'ignored'

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

    heatmap = sample_to_heatmap(sample_points)
    plot_heatmap(heatmap, save_path=heatmap_img_path)

    return 'done'


if __name__ == '__main__':
    load_dotenv('.env.local')

    sample_root = Path(os.getenv('SAMPLE_ROOT'))
    output_root = Path(os.getenv('OUTPUT_ROOT'))

    stl_paths = [(stl_path, printer_dir) for printer_dir in printer_dirs(sample_root)
                 for stl_path in list(printer_dir.glob('**/*.STL'))]

    Parallel(n_jobs=os.cpu_count())(delayed(process_stl)(stl_path, printer_dir) for stl_path, printer_dir in stl_paths)
