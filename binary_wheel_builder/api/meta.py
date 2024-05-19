"""
Meta data around wheels
"""
import functools
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field, GetJsonSchemaHandler, dataclasses
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


@dataclasses.dataclass(frozen=True)
class WheelPlatformBuildResult:
    """Result of a wheel file build"""

    checksum: str
    """Contains the SHA256 checksum of the created wheel file"""

    file_path: Path
    """Full qualified path to wheel"""


@dataclasses.dataclass(frozen=True)
class WheelPlatformIdentifier:
    """Identifies a wheel target platform"""

    platform: str = Field(description="Name of the platform")
    """Name of the platform"""

    python_tag: str = Field(default="py3", description="Python tag (e.g pyX)")
    """Python tag (e.g pyX)"""

    abi_tag: str = Field(
        default="none",
        description="Indicates which Python ABI is required by any included extension modules."
    )
    """Indicates which Python ABI is required by any included extension modules."""

    def to_tag(self):
        """Build to python wheel tag format"""
        return "-".join(
            [
                self.python_tag,
                self.abi_tag,
                self.platform,
            ]
        )


class WheelFileEntry(BaseModel):
    """Source entry for a wheel"""

    path: str = Field(description="Path of the file in the wheel")
    """Path of the file in the wheel"""

    content: bytes = Field(description="Binary content for the file")
    """Binary content for the file"""

    permissions: int = Field(0o644, description="Permissions for the file in the archive")
    """Permissions for the file in the archive"""


class WheelSource(ABC):
    """
    Represents a source that can be used to build a wheel around
    """

    @abstractmethod
    def generate_fileset(self, wheel_platform: WheelPlatformIdentifier) -> list[WheelFileEntry]:
        """
        Generate a list of files to add to the wheel
        :param wheel_platform: Platform of the wheel the files will be used on
        :return: List with wheel file entries for adding to the wheel archive
        """
        return []

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: core_schema.JsonSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = {}
        json_schema.update(type="object", required=[], properties={})
        return json_schema

    @classmethod
    def validate(
            cls, __input_value: Any, _: core_schema.ValidationInfo
    ) -> "WheelSource":
        if not isinstance(__input_value, cls):
            raise ValueError(f"Expected WheelSource, received: {type(__input_value)}")
        return __input_value

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            source: type[Any],
            handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)


@dataclasses.dataclass(frozen=True)
class Wheel:
    """
    Metadata about a wheel to generate
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    package: str = Field(description="Name of the generated package")
    """Name of the generated package"""

    executable: str = Field(
        description="Path of the executable, relative to the package folder. It must match one of "
                    "the file names from the wheel sources in order to work"
    )
    """Path of the executable, relative to the package folder. 
    It must match one of the file names from the wheel sources in order to work"""

    name: str = Field(description="Name of the wheel package")
    """Name of the wheel package"""

    version: str = Field(description="Version of the package")
    """Version of the package"""

    source: WheelSource = Field(description="Source to fetch files from")
    """Source to fetch files from"""

    platforms: Sequence[WheelPlatformIdentifier] = Field(description="Platforms supported by the wheel")
    """Platforms supported by the wheel"""

    summary: str | None = Field(None, description="Summary for package metadata")
    """Summary for package metadata"""

    description: str | None = Field(None, description="Description for package metadata")
    """Description for package metadata"""

    license: str | None = Field(None, description="Name of the license")
    """Name of the license"""

    classifier: Sequence[str] | None = Field(None, description="Classifiers to show in frontends")
    """Classifiers to show in frontends"""

    project_urls: dict[str, str] | None = Field(None, description="Include project URLs like bugtrackers etc.")
    """Include project URLs like bugtrackers etc."""

    requires_python: str | None = Field(None, description="Python version constraint for the wheel")
    """Python version constraint for the wheel"""

    add_to_path: bool = Field(True, description="Should the executable be added to the path (using python wrapper)")
    """Should the executable be added to the path (using python wrapper)"""

    @functools.cached_property
    def normalized_name(self):
        """
        Normalize the name for use in wheel naming
        :return: Replaced all dashes with underscores
        """
        return self.name.replace("-", "_")

    @functools.cached_property
    def dist_info_folder(self):
        """
        Get dist info folder inside wheel based on normalized name and version
        :return:
        """
        return f'{self.normalized_name}-{self.version}.dist-info'

    def wheel_filename(self, tag: str):
        """
        Build wheel filename for given wheel tag
        :param tag: Tag to append to file name
        :return: File name without parent folder for wheel archive
        """
        return f'{self.normalized_name}-{self.version}-{tag}.whl'
