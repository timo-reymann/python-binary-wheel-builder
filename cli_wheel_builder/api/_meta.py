import dataclasses
from abc import abstractmethod, ABC
from pathlib import Path
from typing import Sequence


@dataclasses.dataclass
class WheelPlatformBuildResult:
    checksum: str
    """Contains the SHA256 checksum of the created wheel file"""
    file_path: Path
    """Full qualified path to wheel"""


@dataclasses.dataclass(frozen=True)
class WheelPlatformIdentifier:
    platform: str
    """Name of the platform"""
    python_tag: str = "py3"
    """Python tag pyXx"""
    abi_tag: str = "none"
    """ABI tag"""

    def to_tag(self):
        """Build to python wheel tag format"""
        return "-".join([
            self.python_tag,
            self.abi_tag,
            self.platform,
        ])


@dataclasses.dataclass
class WheelFileEntry:
    path: str
    """Path of the file in the wheel"""
    content: bytes
    """Binary content for the file"""
    permissions: int = 0o644
    """Permissions for the file in the archive"""


class WheelSource(ABC):
    @abstractmethod
    def generate_fileset(self, wheel_platform: WheelPlatformIdentifier) -> list[WheelFileEntry]:
        """
        Generate a list of files to add to the wheel
        :param wheel_platform: Platform of the wheel the files will be used on
        :return: List with wheel file entries for adding to the wheel archive
        """
        return []


@dataclasses.dataclass
class Wheel:
    package: str
    """Name of the generated package"""
    executable: str
    """Relative path of the executable"""
    name: str
    """Name of the pypi package"""
    version: str
    """Version of the package"""
    source: WheelSource
    """Source to fetch files from"""
    platforms: Sequence[WheelPlatformIdentifier]
    """Platforms supported by the wheel"""
    summary: str | None = None
    """Summary for package metadata"""
    description: str | None = None
    """Description for package metadata"""
    license: str | None = None
    """Name of the license"""
    classifier: Sequence[str] | None = None
    """Classifiers to show in frontends"""
    project_urls: dict[str, str] | None = None
    """Incude project URLs like bugtrackers etc."""
    requires_python: str | None = None
    """Python version constraint for the wheel"""
    add_to_path: bool = True
    """Should the executable be added to the path (using python wrapper)"""
