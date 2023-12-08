import dataclasses
from abc import abstractmethod, ABC
from pathlib import Path
from typing import Sequence


@dataclasses.dataclass
class WheelPlatformBuildResult:
    checksum: str
    file_path: Path


@dataclasses.dataclass
class WheelPlatformIdentifier:
    platform: str
    python_tag: str = "py3"
    abi_tag: str = "none"

    def to_tag(self):
        return "-".join([
            self.python_tag,
            self.abi_tag,
            self.platform,
        ])


class WheelSource(ABC):
    @abstractmethod
    def generate_fileset(self, wheel_platform: WheelPlatformIdentifier) -> dict[str, bytes]:
        return {}


@dataclasses.dataclass
class Wheel:
    package: str
    executable: str
    name: str
    version: str
    source: WheelSource
    platforms: Sequence[WheelPlatformIdentifier]
    summary: str | None = None
    description: str | None = None
    license: str | None = None
    classifier: Sequence[str] | None = None
    project_urls: Sequence[str] | None = None
    requires_python: str | None = None
