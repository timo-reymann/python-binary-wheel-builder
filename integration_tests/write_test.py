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
        'dummy-0.0.1-py3-none-win32.whl': '3cd1b22d880fe35522665ef4b9cdb7c9ac0e53efb7cfe25f19301b8f5d66e3f5',
        'dummy-0.0.1-py3-none-win_amd64.whl': 'a25c1a0cd4a8be99a232e42a3b1d97753067c1d6b7c930f640054d546a2ab9a4',
        'dummy-0.0.1-py3-none-macosx_10_9_x86_64.whl': '9adaa4005c2e984fe61036434119f9132e421fbe16ba1cabf56fcd79da78563e',
        'dummy-0.0.1-py3-none-macosx_11_0_arm64.whl': 'ed7672a6217cb75acfaa27f0ead3de24e60b43f512495e0a291f817f3b34d8ef',
        'dummy-0.0.1-py3-none-manylinux_2_12_i686.manylinux2010_i686.whl': '22df4bffab30793bc12df1dcadc7b1dd58bf84cf1fefebd1379ad687a1fad302',
        'dummy-0.0.1-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl': 'df81ebab9b5d98d43e640e5e64b487b450156320bf561077ae720a6b9cd10140',
        'dummy-0.0.1-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl': 'b845334fc93059c31a32be4b887a1ade91429dcb793e89b67e6c51f4a010ab57',
        'dummy-0.0.1-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl': 'bdf0cb9569d4fefcb99da0277a667eacafe04f5287396e9a3b4bd72c46e891cd',
    }

    def test_idempotent_creation(self):
        script_path = os.path.abspath(__file__)
        folder_name = os.path.basename(os.path.dirname(script_path))
        temp_path = Path(tempfile.mktemp())

        for result in build_wheel(Wheel(
                package="dummy",
                executable="dummy",
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
                    well_known_platforms.MAC_SILICON,
                    well_known_platforms.LINUX_GENERIC_i386,
                    well_known_platforms.LINUX_GENERIC_x86_64,
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
