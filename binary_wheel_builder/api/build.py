from pathlib import Path
from typing import Generator

from binary_wheel_builder.api._wheel_extensions import _create_all_supported_platform_wheels
from binary_wheel_builder.api.meta import Wheel, WheelPlatformBuildResult


def build_wheel(wheel_meta: Wheel, dist_folder: Path) -> Generator[WheelPlatformBuildResult, None, None]:
    """
    Build a given wheel based on metadata and write all wheels to the dist folder.

    As this is a generator, make sure to consume all results to ensure all wheels are built properly.

    :param wheel_meta: Metadata about wheel, used to construct the wheel archive for each platform.
    :param dist_folder: Path where all wheel files will be created
    :return: Yields for each generated platform wheel
    """
    dist_folder.mkdir(exist_ok=True)
    for result in _create_all_supported_platform_wheels(wheel_meta, dist_folder):
        yield result
