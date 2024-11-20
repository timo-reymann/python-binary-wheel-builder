"""
Infrastructure to build deterministic wheels
"""
import concurrent.futures
import hashlib
import os
from collections.abc import Generator
from operator import attrgetter
from zipfile import Path

from binary_wheel_builder import wrapper_templates
from binary_wheel_builder.api.meta import (Wheel, WheelFileEntry, WheelPlatformBuildResult, WheelPlatformIdentifier,
                                           WheelSource)
from binary_wheel_builder.wheel.reproducible import ReproducibleWheelFile
from binary_wheel_builder.wheel.util import generate_metadata_file, generate_wheel_file


def _write_wheel(
        out_dir: str,
        wheel: Wheel,
        tag: str,
        metadata: dict,
        wheel_file_entries: list[WheelFileEntry]
):
    wheel_file_path = os.path.join(out_dir, wheel.wheel_filename(tag))

    entries = [
        *wheel_file_entries,
        WheelFileEntry(
            path=f'{wheel.dist_info_folder}/METADATA',
            content=generate_metadata_file(wheel.name, wheel.normalized_version, wheel.description, **metadata)
        ),
        WheelFileEntry(
            path=f'{wheel.dist_info_folder}/WHEEL',
            content=generate_wheel_file(tag)
        )
    ]

    with ReproducibleWheelFile(wheel_file_path, 'w') as wheel_file:
        for wheel_entry in sorted(entries, key=attrgetter('path')):
            wheel_file.write_content_file(wheel_entry)

    return wheel_file_path


def _write_platform_wheel_with_wrappers(
        out_dir: str,
        wheel_info: Wheel,
        platform: WheelPlatformIdentifier,
        source: WheelSource
):
    contents = [
        WheelFileEntry(
            path=f'{wheel_info.package}/__init__.py',
            content=b''
        ),
        WheelFileEntry(
            path=f'{wheel_info.package}/__main__.py',
            content=wrapper_templates.module_main(wheel_info)
        ),
        WheelFileEntry(
            path=f'{wheel_info.package}/exec.py',
            content=wrapper_templates.exec_util(wheel_info)
        )
    ]

    if wheel_info.add_to_path:
        contents.append(
            WheelFileEntry(
                path=f'{wheel_info.dist_info_folder}/entry_points.txt',
                content=wrapper_templates.entry_points_txt(wheel_info)
            )
        )

    return _write_wheel(
        out_dir=out_dir,
        wheel=wheel_info,
        tag=platform.to_tag(),
        metadata={
            'Summary': wheel_info.summary,
            'Description-Content-Type': 'text/markdown',
            'License': wheel_info.license,
            'Classifier': wheel_info.classifier,
            'Project-URL': wheel_info.project_urls,
            'Requires-Python': wheel_info.requires_python,
        },
        wheel_file_entries=[
            *contents,
            # we append the package prefix to all generated files to make sure that they are in scope and reachable
            *[
                f.model_copy(update={'path': wheel_info.package + "/" + f.path})
                for f in source.generate_fileset(platform)]
        ],
    )


def build_wheel(wheel_meta: Wheel, dist_folder: Path, worker_count: int = 1) -> Generator[WheelPlatformBuildResult, None, None]:
    """
    Build a given wheel based on metadata and write all wheels to the dist folder.

    As this is a generator, make sure to consume all results to ensure all wheels are built properly.

    :param wheel_meta: Metadata about wheel, used to construct the wheel archive for each platform.
    :param dist_folder: Path where all wheel files will be created
    :param worker_count: Amount of workers to run wheel builds in parallel
    :return: Yields for each generated platform wheel
    """
    dist_folder.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [
            executor.submit(
                _build_wheel_for_platform,
                dist_folder,
                python_platform,
                wheel_meta
            )
            for python_platform in wheel_meta.platforms
        ]
        for future in concurrent.futures.as_completed(futures):
            yield future.result()



def _build_wheel_for_platform(dist_folder, python_platform, wheel_meta):
    wheel_path = _write_platform_wheel_with_wrappers(
        dist_folder.__str__(),
        wheel_meta,
        python_platform,
        wheel_meta.source,
    )
    with open(wheel_path, 'rb') as wheel:
        return WheelPlatformBuildResult(
            checksum=hashlib.sha256(wheel.read()).hexdigest(),
            file_path=wheel_path,
        )
