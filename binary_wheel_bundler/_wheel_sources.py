import urllib
from pathlib import Path

from binary_wheel_bundler import WheelSource, WheelPlatformIdentifier, well_known_platforms


class StaticLocalWheelSource(WheelSource):
    def __init__(self, file: Path):
        self.file = file

    def generate_fileset(self, _: WheelPlatformIdentifier) -> dict[str, bytes]:
        return {
            self.file.name: self.file.read_bytes()
        }
