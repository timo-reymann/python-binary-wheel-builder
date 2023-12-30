from pathlib import Path

from binary_wheel_builder.api.meta import WheelSource, WheelPlatformIdentifier, WheelFileEntry


class StaticLocalWheelSource(WheelSource):
    def __init__(self, file: Path):
        self.file = file

    def generate_fileset(self, _: WheelPlatformIdentifier) -> list[WheelFileEntry]:
        return [
            WheelFileEntry(
                path=self.file.name,
                content=self.file.read_bytes()
            )
        ]
