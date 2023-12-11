import tempfile
from pathlib import Path
from unittest import TestCase
from urllib.request import urlopen

from binary_wheel_bundler import well_known_platforms, create_all_supported_platform_wheels, build
from binary_wheel_bundler import WheelSource, WheelPlatformIdentifier, Wheel, WheelFileEntry


class BufGithubReleaseSource(WheelSource):
    def __init__(self, version: str):
        self.version = version

    def generate_fileset(self, wheel_platform: WheelPlatformIdentifier) -> list[WheelFileEntry]:
        os_name = None
        arch = None

        match wheel_platform:
            case well_known_platforms.MAC_SILICONE:
                os_name = 'Darwin'
                arch = "arm64"
            case well_known_platforms.MAC_INTEL:
                os_name = 'Darwin'
                arch = "x86_64"
            case well_known_platforms.WINDOWS_x86_64:
                os_name = 'Windows'
                arch = "x86_64.exe"
            case well_known_platforms.LINUX_GENERIC_x84_64:
                os_name = 'Linux'
                arch = "x86_64"
            case well_known_platforms.LINUX_GENERIC_aarch64 | well_known_platforms.LINUX_GENERIC_armv7a:
                os_name = 'Linux'
                arch = "aarch64"
        url = f"https://github.com/bufbuild/buf/releases/download/v{self.version}/buf-{os_name}-{arch}"

        with urlopen(url) as response:
            file_content = response.read()

        return [
            WheelFileEntry(
                path="buf/buf",
                content=file_content,
                permissions=0o755
            )
        ]


class GitHubReleasesTest(TestCase):
    def test_buf(self):
        for result in build(
                Wheel(
                    package="buf",
                    executable="buf",
                    name="buf",
                    version="0.0.1",
                    summary='Buf cli wrapped',
                    license='MIT',
                    requires_python=">=3.9",
                    classifier=[
                        'License :: OSI Approved :: MIT License',
                    ],
                    project_urls=[
                        'Homepage, https://example.com',
                        'Source Code, https://github.com/examle/example',
                        'Bug Tracker, https://github.com/example/example/issues',
                    ],
                    source=BufGithubReleaseSource("1.28.1"),
                    platforms=[
                        well_known_platforms.WINDOWS_x86_64,
                        well_known_platforms.MAC_INTEL,
                        well_known_platforms.MAC_SILICONE,
                        well_known_platforms.LINUX_GENERIC_x84_64,
                    ]
                ),
                Path(tempfile.mkdtemp())
        ):
            print(result)
