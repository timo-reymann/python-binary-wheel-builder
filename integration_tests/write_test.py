import os
import platform
import tempfile
import unittest
from pathlib import Path

from binary_wheel_builder import Wheel, build_wheel
from binary_wheel_builder import well_known_platforms
from binary_wheel_builder.api.wheel_sources import StaticLocalWheelSource
from integration_tests.util import verify_wheel_structure, install_wheel


class WriteTest(unittest.TestCase):
    expected_checksums = {
        'dummy-0.0.1-py3-none-win32.whl': '89281b59a4fa3d987c210b327e8f8d56ceb5bb700adbc4b07944e046813e37e2',
        'dummy-0.0.1-py3-none-win_amd64.whl': '249e41c5bb60d05f2f20a9e0dc7a2c52a77c6f42b2c8fc25436dd88c6f3cad1e',
        'dummy-0.0.1-py3-none-macosx_10_9_x86_64.whl': '4043d8e4e92642de5496d272343276831bca871c052c465c405add2826d57167',
        'dummy-0.0.1-py3-none-macosx_11_0_arm64.whl': '8bd1338a3f18d83f94ff38baab94ce526f47bd3d3d7725855f6aebec3e5fcc6e',
        'dummy-0.0.1-py3-none-manylinux_2_12_i686.manylinux2010_i686.whl': '162ecb64acd76634d601c6e34c64d701ed08ebea2d7b54421a72808e29683896',
        'dummy-0.0.1-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl': 'd1471277a4d0b2c7e8a96a06ed27a737d58a00c07fac4f15f26734bebeeb7d33',
        'dummy-0.0.1-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl': 'cf9dc106bf137145c3ba90aebb50e9f85ac750be947146dc6c2e1016479b2af3',
        'dummy-0.0.1-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl': '8e1fd4e65e192d90e394722df355112605012e61fcb55d778c521b1ce0cfefa8',
    }

    def test_idempotent_creation(self):
        script_path = os.path.abspath(__file__)
        folder_name = os.path.basename(os.path.dirname(script_path))
        temp_path = Path(tempfile.mktemp())

        for result in build_wheel(Wheel(
                package="dummy",
                executable="dummy/dummy",
                name="dummy",
                version="0.0.1",
                summary='Dummy is showcasing how it could look like',
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
                source=StaticLocalWheelSource(Path(f"{folder_name}/testdata/dummy")),
                platforms=[
                    well_known_platforms.WINDOWS_i386,
                    well_known_platforms.WINDOWS_x86_64,
                    well_known_platforms.MAC_INTEL,
                    well_known_platforms.MAC_SILICONE,
                    well_known_platforms.LINUX_GENERIC_i386,
                    well_known_platforms.LINUX_GENERIC_x84_64,
                    well_known_platforms.LINUX_GENERIC_armv7a,
                    well_known_platforms.LINUX_GENERIC_aarch64,
                ],
                add_to_path=False,
        ), temp_path):
            print(result)

            verify_wheel_structure(
                result.file_path,
                [
                    ('dummy-0.0.1.dist-info/RECORD', 0o644),
                    ('dummy-0.0.1.dist-info/METADATA', 0o644)
                ], [
                    'dummy-0.0.1.dist-info/entry_points.txt'
                ]
            )

            install_wheel(result.file_path.parent, "dummy")

            if platform.system() != "Windows":
                self.assertEqual(self.expected_checksums[Path(result.file_path).name], result.checksum)
