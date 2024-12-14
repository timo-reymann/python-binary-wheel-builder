import logging
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from binary_wheel_builder import __version__
from binary_wheel_builder.api import build_wheel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _parse_args(args) -> Namespace:
    parser = ArgumentParser("CLI Wheel Builder")
    parser.add_argument(
        "--wheel-spec",
        type=str,
        required=True,
        help="Path to the wheel specification file",
    )
    parser.add_argument(
        "--dist-folder",
        default="dist/",
        type=str,
        help="Folder to store the built wheels in",
    )
    parser.add_argument(
        "--max-workers",
        default=4,
        type=int,
        help="Number of parallel workers to use at most for building wheels"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__
    )
    return parser.parse_args(args)


def main(argv=None) -> None:
    try:
        import yaml
    except:
        raise SystemExit("PyYAML not installed, can not use CLI.")

    if argv is None:
        argv = sys.argv[1:] if sys.argv else []

    args = _parse_args(argv)

    dist_path = Path(args.dist_folder)
    
    try:
        dist_path.mkdir(exist_ok=True)
    except OSError as e:
        raise SystemExit(f"Failed to create dist folder at '{dist_path}': {e}")

    from binary_wheel_builder.cli.config_file import load_wheel_spec_from_yaml
     
    try:
        wheel = load_wheel_spec_from_yaml(Path(args.wheel_spec))
    except Exception as e:
        raise SystemExit(f"Failed to load wheel spec from '{args.wheel_spec}': {e}")

    try:
        for result in build_wheel(wheel, dist_path, worker_count=args.max_workers):
            print(f"> {result.checksum} - {result.file_path}")
    except Exception as e:
        raise SystemExit(f"Error occurred while building wheels: {e}")
