from pathlib import Path

from cli_wheel_builder._meta import WheelSource, WheelPlatformIdentifier, WheelFileEntry


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


class GithubReleaseBinarySource(WheelSource):
    def __init__(self,
                 project_slug: str,
                 version: str,
                 asset_name_mapping: dict[WheelPlatformIdentifier, str],
                 binary_path: str,
                 tag_prefix="v", ):
        self.project_slug = project_slug
        self.version = version
        self.tag_prefix = tag_prefix
        self.asset_name_mapping = asset_name_mapping
        self.binary_path = binary_path

    def generate_fileset(self, wheel_platform: WheelPlatformIdentifier) -> list[WheelFileEntry]:
        from urllib.request import urlopen

        if wheel_platform not in self.asset_name_mapping:
            print(self.asset_name_mapping)
            raise Exception(wheel_platform)

        url = (f"https://github.com/{self.project_slug}"
               f"/releases/download/{self.tag_prefix}{self.version}/{self.asset_name_mapping[wheel_platform]}")

        print(url)
        with urlopen(url) as response:
            file_content = response.read()

        return [
            WheelFileEntry(
                path=self.binary_path,
                content=file_content,
                permissions=0o755
            )
        ]
