import os
import tempfile
import unittest
from pathlib import Path

from binary_wheel_bundler import Wheel, StaticLocalWheelSource, build
from binary_wheel_bundler import well_known_platforms


class WriteTest(unittest.TestCase):
    expected_checksums = {
        'dummy-0.0.1-py3-none-win32.whl': 'e13d9e65439d58d713998d606568a3addf09d62eb208774151ad0507af26eead',
        'dummy-0.0.1-py3-none-win_amd64.whl': '6b0846627633050aceec845e28abd77cc3f973309f6925c32fe41d872bfc335d',
        'dummy-0.0.1-py3-none-macosx_10_9_x86_64.whl': '31fa78bc34b624fa264d0e8f0a80eb4d1952329f85d8cf6766a4a80158fbd038',
        'dummy-0.0.1-py3-none-macosx_11_0_arm64.whl': '065913e1c2db92d2492e8f6e2dba390b2dadc75b4934bc1c73dd9aee55662385',
        'dummy-0.0.1-py3-none-manylinux_2_12_i686.manylinux2010_i686.whl': 'de80927d4f57cac9743f49e17058b7759239dbaec85d0ef11e06a56ee801e9cd',
        'dummy-0.0.1-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl': 'ee6bf170438b75969a4bcd4af55dcb9893248b94952251673e71530489aca517',
        'dummy-0.0.1-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl': 'a7c525ad50a53f0bb579e4562dc597cc0f24d60352f04960e8713569e060a00a',
        'dummy-0.0.1-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl': 'c7d0e87fba66d94d63f69e377aded09940c4587b922bd42e130ce26ecbb5a872',
    }

    def test_idempotent_creation(self):
        script_path = os.path.abspath(__file__)
        folder_name = os.path.basename(os.path.dirname(script_path))
        temp_path = Path(tempfile.mktemp())

        for result in build(Wheel(
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
        ), temp_path):
            self.assertEqual(result.checksum, self.expected_checksums[Path(result.file_path).name])
