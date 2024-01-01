from pathlib import Path

from binary_wheel_builder.api.meta import WheelSource, WheelPlatformIdentifier, WheelFileEntry
from binary_wheel_builder.api.wheel_sources.exceptions import UnsupportedWheelPlatformException, SourceFileRequestFailed


class PlatformBasedFileSource(WheelSource):
    def __init__(self, executable_path : str, file_name_mapping: dict[WheelPlatformIdentifier, Path | str]):
        self.executable_path = executable_path
        self.file_name_mapping = file_name_mapping

    def generate_fileset(self, wheel_platform: WheelPlatformIdentifier) -> list[WheelFileEntry]:
        if wheel_platform not in self.file_name_mapping:
            raise UnsupportedWheelPlatformException(wheel_platform)

        file = self.file_name_mapping[wheel_platform]

        if isinstance(file, str):
            file = Path(file)

        if not file.exists() or not file.is_file():
            raise SourceFileRequestFailed(f"File {file} does not resolve to a valid file")

        return [
            WheelFileEntry(
                path=self.executable_path,
                content=file.read_bytes(),
                permissions=0o755
            )
        ]
