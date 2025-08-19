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
        'dummy-0.0.1-py3-none-win32.whl': '76cb3d98bc018927b228383d3a2c9a300d968bfd6d62ee4b0faa434dcef58616',
        'dummy-0.0.1-py3-none-win_amd64.whl': '8c81cbe4ef4749330ed6891d111da497e17423cd41df13f460879f88d9eded83',
        'dummy-0.0.1-py3-none-macosx_10_9_x86_64.whl': 'f5a5bdd850d3ca9367866ad7950eaa581b0bd28bb990215b903fa27b09c676af',
        'dummy-0.0.1-py3-none-macosx_11_0_arm64.whl': '96a1eaeff73772d9d98cf9bb801b59b67fa53b7df0ffcff01cd3dd3539d5fe9a',
        'dummy-0.0.1-py3-none-manylinux_2_12_i686.manylinux2010_i686.whl': '255f4ed5435486edc70394d24b358bc47c3723051d6a7cfc73cef9ff359fb65f',
        'dummy-0.0.1-py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl': 'cf57ce7304867ec797fde2c3dae70a67ac6688285b0ac0c3176b52e3220323c2',
        'dummy-0.0.1-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl': '3d6a2e155cb2720ac85880a9169cbdfbd578efb604d180a6f23dc4a2f61167f5',
        'dummy-0.0.1-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl': '01f4fe155ac20a017936c84a04221d6847bcfa2dace95bc3d15b6b371c3d6bae',
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
