"""
Source for local binaries, which differ based on the target platform
"""
from pathlib import Path

from binary_wheel_builder.api.meta import WheelFileEntry, WheelPlatformIdentifier, WheelSource
from binary_wheel_builder.api.wheel_sources.exceptions import SourceFileRequestFailed, UnsupportedWheelPlatformException


class PlatformBasedFileSource(WheelSource):
    """
    Provide source from a local file, the name depending on the target platform
    """
    def __init__(self, executable_path: str, file_name_mapping: dict[WheelPlatformIdentifier, Path | str]):
        """

        :param executable_path: Path to the executable that will be used in the generated wheel
        :param file_name_mapping: Map wheel platform identifiers to the local binary file names.
        """
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
