import tempfile
from pathlib import Path

import pytest

from binary_wheel_builder.api import well_known_platforms
from binary_wheel_builder.api.wheel_sources.exceptions import SourceFileRequestFailed
from binary_wheel_builder.api.wheel_sources.platform_based_file import PlatformBasedFileSource


def test_platform_based_file_invalid():
    source = PlatformBasedFileSource("package/test", {
        well_known_platforms.LINUX_GENERIC_i386: Path("linux-x86"),
    })

    with pytest.raises(SourceFileRequestFailed):
        source.generate_fileset(well_known_platforms.LINUX_GENERIC_i386)


def test_platform_based_file_valid():
    with tempfile.NamedTemporaryFile("w") as f:
        f.write("test")
        f.flush()

        source = PlatformBasedFileSource("package/test", {
            well_known_platforms.LINUX_GENERIC_i386: Path(f.name),
        })

        source.generate_fileset(well_known_platforms.LINUX_GENERIC_i386)
