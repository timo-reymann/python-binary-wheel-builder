import os
import platform
import tempfile
import unittest
from pathlib import Path

from binary_wheel_builder import Wheel, build_wheel
from binary_wheel_builder import well_known_platforms
from binary_wheel_builder.api.wheel_sources import StaticLocalWheelSource
from integration_tests.util import verify_wheel_structure


class WriteTest(unittest.TestCase):
    expected_checksums = {
        'dummy-0.0.1-py3-none-win32.whl': '2b6b5511b317b94594e0d47508edccc43b294e8ac12b32910fb7f40f6030facb',
        'dummy-0.0.1-py3-none-win_amd64.whl': '0e5b3c59877a3e1ade955fb9090dc64b89f4a7989d0574b70a82d72eaef4248c',
        'dummy-0.0.1-py3-none-macosx_10_9_x86_64.whl': 'a76739571c86efef8c6aced19d49b9ae2fa21a89d4ab6810336f62e3928c7c87',
        'dummy-0.0.1-py3-none-macosx_11_0_arm64.whl': 'd12f6ce63684efa9eaddfa8bfd7873700d786b833f7fe795ba7f5d3d2c97fce6',
        'dummy-0.0.1-py3-none-manylinux_2_12_i686.manylinux2010_i686.whl': '052e1aecbf09b25284a91799c81f1f8ed73d3045fe8035ccc1d8278ac42290db',
        'dummy-0.0.1-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl': 'fe7243bf6b8d5a8b4bdaed97b3f00515f4319e4fdd1defdba00de1449a6ac033',
        'dummy-0.0.1-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl': '89fd470508068aa8f2b52b0c896c582d7da6629614c4eb3e7a8c9ca6de512627',
        'dummy-0.0.1-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl': '85cce005163ddf8c0460caeafe0520c0e1e44f57956f1710c812a08ef946e22b',
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
            if platform.system() != "Windows":
                self.assertEqual(result.checksum, self.expected_checksums[Path(result.file_path).name])

            verify_wheel_structure(
                result.file_path,
                [
                    ('dummy-0.0.1.dist-info/RECORD', 0o644),
                    ('dummy-0.0.1.dist-info/METADATA', 0o644)
                ], [
                    'dummy-0.0.1.dist-info/entry_points.txt'
                ]
            )
