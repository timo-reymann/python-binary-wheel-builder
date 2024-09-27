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
        'dummy-0.0.1-py3-none-win32.whl': 'd5a5aaf28374721ae0f257bd0bd799e13eba879e91e6de744a522363824de8a1',
        'dummy-0.0.1-py3-none-win_amd64.whl': 'e7cec5b5784c6dde0097314beef784f6961c0d2a6c5e0df432fb921e85d59b09',
        'dummy-0.0.1-py3-none-macosx_10_9_x86_64.whl': 'dc6f7d2116cc251622127816ee1a2e1a8cc8f1c0aa1629ed483fb740625494ab',
        'dummy-0.0.1-py3-none-macosx_11_0_arm64.whl': 'cc924a8dedb73107437a49013b60b701c286047011c67ef89b633fa3b0064e4a',
        'dummy-0.0.1-py3-none-manylinux_2_12_i686.manylinux2010_i686.whl': '18b27a6efce30286fa1b7bb79f09ad6a29ddcc210e615ed7d36c96b264328975',
        'dummy-0.0.1-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl': '88df741fa70fe4696858d4ec8861e8332be99094fdadc8c4a9ba0755ca87e5ae',
        'dummy-0.0.1-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl': '74116eacefbed07dea63c2e9af12326d49ac41b734cf2426d38a2e4ff235bcd6',
        'dummy-0.0.1-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl': '66dde6297c2460c8d461adbb016dbd7d451ca9e58f9a4da31026415228cd7a0f',
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
