from pathlib import Path
from typing import Generator

from binary_wheel_bundler import Wheel, create_all_supported_platform_wheels, WheelPlatformBuildResult


def build(wheel_meta: Wheel, dist_folder: Path) -> Generator[WheelPlatformBuildResult]:
    dist_folder.mkdir(exist_ok=True)
    for result in create_all_supported_platform_wheels(wheel_meta, dist_folder):
        yield result
