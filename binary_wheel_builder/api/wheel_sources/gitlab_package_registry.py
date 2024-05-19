"""
Sources for GitLab
"""
from binary_wheel_builder import WheelFileEntry, WheelPlatformIdentifier, WheelSource
from binary_wheel_builder.api.wheel_sources.exceptions import SourceFileRequestFailed


class GitlabGenericPackageRegistrySource(WheelSource):
    """
    Provide source from Gitlab Generic Package Registry
    """
    def __init__(
            self,
            asset_name_mapping: dict[WheelPlatformIdentifier, str],
            binary_path: str,
            project: int | str,
            version: str,
            package_name: str,
            gitlab_base_url: str = "https://gitlab.com",
            token: str | None = None
    ):
        """
        :param asset_name_mapping: Mapping of the wheel platform to the artifact name from the Gitlab Registry
        :param binary_path: Path to the binary in the target generated wheel
        :param project: Project name or ID
        :param version: Version of the package
        :param package_name: Name of the package
        :param gitlab_base_url: Base URL including protocol, defaults to https://gitlab.com
        :param token: Optional token if you want to access a private package regsitry
        """
        self.artifact_name_mapping = asset_name_mapping
        self.binary_path = binary_path

        if isinstance(project, int):
            self.project = project
        else:
            from urllib.parse import quote
            self.project = quote(project, safe='')

        self.version = version
        self.package_name = package_name
        self.gitlab_base_url = gitlab_base_url
        self.token = token

    def generate_fileset(self, wheel_platform: WheelPlatformIdentifier) -> list[WheelFileEntry]:
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError

        request = Request(
            f"{self.gitlab_base_url}"
            f"/api/v4/projects/{self.project}"
            f"/packages/generic/{self.package_name}"
            f"/{self.version}/{self.artifact_name_mapping[wheel_platform]}"
        )

        if self.token is not None:
            request.add_header("PRIVATE-TOKEN", self.token)

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
