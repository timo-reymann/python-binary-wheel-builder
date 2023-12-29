import os
from binary_wheel_builder.api.meta import WheelFileEntry
from binary_wheel_builder.wheel.util import generate_metafile_content
from binary_wheel_builder.wheel.reproducible import ReproducibleWheelFile


def _write_wheel(
        out_dir: str,
        name: str,
        version: str,
        tag: str,
        metadata: dict,
        description: str,
        wheel_file_entries: list[WheelFileEntry]
):
    normalized_name = name.replace("-", "_")
    wheel_name = f'{normalized_name}-{version}-{tag}.whl'
    dist_info = f'{normalized_name}-{version}.dist-info'
    wheel_file_path = os.path.join(out_dir, wheel_name)

    entries = [
        *wheel_file_entries,
        WheelFileEntry(
            path=f'{dist_info}/METADATA',
            content=generate_metafile_content({
                'Metadata-Version': '2.1',
                'Name': name,
                'Version': version,
                **metadata,
            }, description)
        ),
        WheelFileEntry(
            path=f'{dist_info}/WHEEL',
            content=generate_metafile_content({
                'Wheel-Version': '1.0',
                'Generator': 'ziglang make_wheels.py',
                'Root-Is-Purelib': 'false',
                'Tag': tag,
            })
        )
    ]

    with ReproducibleWheelFile(wheel_file_path, 'w') as wheel_file:
        for wheel_entry in entries:
            wheel_file.write_content_file(wheel_entry)

    return wheel_file_path
