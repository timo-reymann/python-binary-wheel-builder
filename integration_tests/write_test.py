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
        'dummy-0.0.1-py3-none-win32.whl': 'bc9f0cde7d905fd820b8752819eb22f9b64088f912cf04b463743de597b4fe85',
        'dummy-0.0.1-py3-none-win_amd64.whl': 'a79a2c0fe5c01883400980cefec14022998227297e96536aeed2f468e04e3824',
        'dummy-0.0.1-py3-none-macosx_10_9_x86_64.whl': 'c379162257e63a98222de65a01c3e54461124b8579955a7ba9d2f80107b84154',
        'dummy-0.0.1-py3-none-macosx_11_0_arm64.whl': '4b8ca8d7e0ce8559e852178baead909ea4e5e83da063d6a3c6bd0d68eb98c4b5',
        'dummy-0.0.1-py3-none-manylinux_2_12_i686.manylinux2010_i686.whl': 'da5071eb0957d1ff139c2c0283f5e71ec6fc6b763c4cdf79192a407b70102d18',
        'dummy-0.0.1-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl': '2697973602bbfa523a6327b0edbe40f0cb3d469dbd35e1192c9aa2bec8eccaa3',
        'dummy-0.0.1-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl': '2960fd23b9493fbf9e179e585790e79f2185dc9d32a1b2bb6d4dcabae7ba104a',
        'dummy-0.0.1-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl': '7b66bff256800fdb9ecf1c2d60733d31cd709b2072f1aafc544d64c43f26c874',
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
