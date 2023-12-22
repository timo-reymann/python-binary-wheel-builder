import tempfile
from pathlib import Path
from unittest import TestCase

from cli_wheel_builder import Wheel, GithubReleaseBinarySource
from cli_wheel_builder import well_known_platforms, build


class BufGithubReleaseSource(GithubReleaseBinarySource):
    def __init__(self, version: str):
        super().__init__("bufbuild/buf",
                         version,
                         {
                             well_known_platforms.MAC_SILICONE: "buf-Darwin-arm64",
                             well_known_platforms.MAC_INTEL: "buf-Darwin-x86_64",
                             well_known_platforms.WINDOWS_x86_64: "buf-Windows-x86_64.exe",
                             well_known_platforms.LINUX_GENERIC_x84_64: "buf-Linux-x86_64",
                             well_known_platforms.LINUX_GENERIC_aarch64: "buf-Linux-aarch64",
                             well_known_platforms.LINUX_GENERIC_armv7a: "buf-Linux-aarch64",
                         },
                         "buf/buf")


class DeterministicZipGitHubReleaseSource(GithubReleaseBinarySource):
    def __init__(self, version: str):
        super().__init__("timo-reymann/deterministic-zip",
                         version,
                         {
                             well_known_platforms.MAC_SILICONE: "deterministic-zip_darwin-amd64",
                             well_known_platforms.MAC_INTEL: "deterministic-zip_darwin-arm64",
                             well_known_platforms.LINUX_GENERIC_x84_64: "deterministic-zip_linux-amd64",
                             well_known_platforms.LINUX_GENERIC_aarch64: "deterministic-zip_linux-arm",
                             well_known_platforms.LINUX_GENERIC_armv7a: "deterministic-zip_linux-arm",
                         },
                         "deterministic_zip/deterministic-zip",
                         "")


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
                    project_urls={
                        'Homepage': 'https://example.com',
                        'Source Code': ' https://github.com/examle/example',
                        'Bug Tracker': ' https://github.com/example/example/issues',
                    },
                    source=BufGithubReleaseSource("1.28.1"),
                    platforms=[
                        well_known_platforms.MAC_INTEL,
                        well_known_platforms.WINDOWS_x86_64,
                        well_known_platforms.MAC_SILICONE,
                        well_known_platforms.LINUX_GENERIC_x84_64,
                    ]
                ),
                Path(tempfile.mkdtemp())
        ):
            print(result)

    def test_zip(self):
        for result in build(
                Wheel(
                    package="deterministic_zip",
                    executable="deterministic-zip",
                    name="deterministic-zip",
                    version="0.0.1",
                    summary='deterministic-zip cli wrapped',
                    license='MIT',
                    requires_python=">=3.9",
                    classifier=[
                        'License :: OSI Approved :: MIT License',
                    ],
                    project_urls={
                        'Homepage': ' https://example.com',
                        'Source Code': ' https://github.com/examle/example',
                        'Bug Tracker': ' https://github.com/example/example/issues',
                    },
                    source=DeterministicZipGitHubReleaseSource("2.1.0"),
                    platforms=[
                        well_known_platforms.MAC_INTEL,
                        well_known_platforms.MAC_SILICONE,
                        well_known_platforms.LINUX_GENERIC_x84_64,
                    ]
                ),
                Path(tempfile.mkdtemp())
        ):
            print(result)
