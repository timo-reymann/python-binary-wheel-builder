import hashlib
from typing import Sequence
from zipfile import Path

from binary_wheel_bundler._meta import WheelSource, WheelPlatformIdentifier, WheelPlatformBuildResult, Wheel
from binary_wheel_bundler._wheel_util import _write_wheel


def _write_platform_wheel(out_dir: str, wheel_info: Wheel, platform: WheelPlatformIdentifier, source: WheelSource):
    contents = {
        f'{wheel_info.package}/__init__.py': b'',
        f'{wheel_info.package}/__main__.py': f'''\
import os, sys, subprocess
sys.exit(subprocess.call([
    os.path.join(os.path.dirname(__file__), "{wheel_info.executable}"),
    *sys.argv[1:]
]))
'''.encode('utf-8')
    }

    for file, content in source.generate_fileset(platform).items():
        contents[wheel_info.package + "/" + file] = content

    return _write_wheel(
        out_dir,
        name=wheel_info.name,
        version=wheel_info.version,
        tag=platform.to_tag(),
        metadata={
            'Summary': wheel_info.summary,
            'Description-Content-Type': 'text/markdown',
            'License': wheel_info.license,
            'Classifier': wheel_info.classifier,
            'Project-URL': wheel_info.project_urls,
            'Requires-Python': wheel_info.requires_python,
        },
        description=wheel_info.description,
        contents=contents,
    )


def create_all_supported_platform_wheels(wheel_meta: Wheel, dist_folder: Path) -> Sequence[WheelPlatformBuildResult]:

    for python_platform in wheel_meta.platforms:
        wheel_path = _write_platform_wheel(
            dist_folder.__str__(),
            wheel_meta,
            python_platform,
            wheel_meta.source,
        )
        with open(wheel_path, 'rb') as wheel:
            yield WheelPlatformBuildResult(
                checksum=hashlib.sha256(wheel.read()).hexdigest(),
                file_path=wheel_path,
            )
