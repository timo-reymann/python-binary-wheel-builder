"""
Sources for GitHub
"""
from urllib.error import HTTPError

from binary_wheel_builder.api.meta import WheelFileEntry, WheelPlatformIdentifier, WheelSource
from binary_wheel_builder.api.wheel_sources.exceptions import SourceFileRequestFailed, UnsupportedWheelPlatformException


class GithubReleaseBinarySource(WheelSource):
    """
    Provide source from GitHub Release API
    """
    def __init__(
            self,
            project_slug: str,
            version: str,
            asset_name_mapping: dict[WheelPlatformIdentifier, str],
            binary_path: str,
            tag_prefix: str = "v",
            token: str | None = None,
    ):
        """
        :param project_slug: Full name of the project e.g. user/project or org/project
        :param version: Version of the release
        :param asset_name_mapping: Mapping of GitHub Release assets to the corresponding wheel platform
        :param binary_path: Path to the binary file in the generated wheel
        :param tag_prefix: Prefix for release tag which will be prepended to version for the version
        :param token: Optional token in case you want to access a private repository
        """
        self.project_slug = project_slug
        self.version = version
        self.asset_name_mapping = asset_name_mapping
        self.binary_path = binary_path
        self.tag_prefix = tag_prefix
        self.token = token

    def generate_fileset(self, wheel_platform: WheelPlatformIdentifier) -> list[WheelFileEntry]:
        from urllib.request import urlopen, Request

        if wheel_platform not in self.asset_name_mapping:
            raise UnsupportedWheelPlatformException(wheel_platform)

        url = (f"https://github.com/{self.project_slug}"
               f"/releases/download/{self.tag_prefix}{self.version}/{self.asset_name_mapping[wheel_platform]}")
        request = Request(url)

        if self.token is not None:
            request.add_header("Authorization", f"token {self.token}")

        try:
            with urlopen(request) as response:
                file_content = response.read()
        except HTTPError as e:
            raise SourceFileRequestFailed("Failed to fetch file: " + str(e)) from e

        return [
            WheelFileEntry(
                path=self.binary_path,
                content=file_content,
                permissions=0o755
            )
        ]
