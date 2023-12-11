import os
import stat
from email.message import EmailMessage
from zipfile import ZipInfo, ZIP_DEFLATED

from wheel.wheelfile import WheelFile

from binary_wheel_bundler._meta import WheelFileEntry


def _generate_metafile_content(headers: dict[str, str], payload=None) -> bytes:
    msg = EmailMessage()
    for name, value in headers.items():
        if isinstance(value, list):
            for value_part in value:
                msg[name] = value_part
        else:
            msg[name] = value
    if payload:
        msg.set_payload(payload)
    return str(msg).encode("utf8")


class ReproducibleWheelFile(WheelFile):
    def write_content_file(self, wheel_entry: WheelFileEntry) -> None:
        zip_info = ZipInfo(wheel_entry.path)
        zip_info.external_attr = (wheel_entry.permissions | stat.S_IFREG) << 16
        zip_info.file_size = len(wheel_entry.content)
        self.writestr(zip_info, data=wheel_entry.content)

    def writestr(self, zip_info: ZipInfo | str, *args, **kwargs):
        if isinstance(zip_info, str):
            zip_info = ZipInfo(zip_info)
            zip_info.external_attr = (0o644 | stat.S_IFREG) << 16
        zip_info.compress_type = self.compression
        zip_info.date_time = (1980, 1, 1, 0, 0, 0)
        zip_info.create_system = 3
        super().writestr(zip_info, *args, **kwargs)


def _write_wheel(
        out_dir: str,
        name: str,
        version: str,
        tag: str,
        metadata: dict,
        description: str,
        wheel_file_entries: list[WheelFileEntry]
):
    wheel_name = f'{name}-{version}-{tag}.whl'
    dist_info = f'{name}-{version}.dist-info'
    wheel_file_path = os.path.join(out_dir, wheel_name)

    entries = [
        *wheel_file_entries,
        WheelFileEntry(
            path=f'{dist_info}/METADATA',
            content=_generate_metafile_content({
                'Metadata-Version': '2.1',
                'Name': name,
                'Version': version,
                **metadata,
            }, description)
        ),
        WheelFileEntry(
            path=f'{dist_info}/WHEEL',
            content=_generate_metafile_content({
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
