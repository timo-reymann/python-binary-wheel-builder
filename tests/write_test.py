import os
import tempfile
import unittest
from pathlib import Path

from binary_wheel_bundler import Wheel, StaticLocalWheelSource
from binary_wheel_bundler import well_known_platforms, create_all_supported_platform_wheels


class WriteTest(unittest.TestCase):
    def test_idempotent_creation(self):
        script_path = os.path.abspath(__file__)
        folder_name = os.path.basename(os.path.dirname(script_path))

        wheel_meta = Wheel(
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
            project_urls=[
                'Homepage, https://example.com',
                'Source Code, https://github.com/examle/example',
                'Bug Tracker, https://github.com/example/example/issues',
            ],
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
            ]
        )

        expected_checksums = {
            'dummy-0.0.1-py3-none-win32.whl': '4b8332ccd3b8f2e000a19a776b2c46f5deea74dd117f5be56051879ee73ac7da',
            'dummy-0.0.1-py3-none-win_amd64.whl': '2be3df6a934a2cac4be285f6ad4a3cdbc68ba60e99f2bb81ea0d0ef55897007f',
            'dummy-0.0.1-py3-none-macosx_10_9_x86_64.whl': '9934731b51b1c85784fa9630a46ca07da5c9a8caec60490af13c51ba0f84bd91',
            'dummy-0.0.1-py3-none-macosx_11_0_arm64.whl': 'c656f277e3a629d3006e882a3d63b27d1ef580786608ec80100d5443e94c516b',
            'dummy-0.0.1-py3-none-manylinux_2_12_i686.manylinux2010_i686.whl': 'b708abff3f8ac1a9db17a05d0703354c5dd8744d9511d4638865114784329acb',
            'dummy-0.0.1-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl': '1ee0e2913e90e5614ef6927459a8c0d7f1a90fe33714011a4e4a85f821b5421a',
            'dummy-0.0.1-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl': '254f73a264c3cb091f8dcd029db39cab9ba5668de2f63cb86b1745262ded565e',
            'dummy-0.0.1-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl': 'eb23bf8b5768f59701bbee76c64902a05e0f6f0fce3ff64771a300dff771fa48',
        }

        temp_path = Path(tempfile.mktemp())
        temp_path.mkdir()
        for result in create_all_supported_platform_wheels(wheel_meta, temp_path):
            self.assertEqual(result.checksum, expected_checksums[Path(result.file_path).name])
