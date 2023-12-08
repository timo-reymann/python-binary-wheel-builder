import os
import stat
from email.message import EmailMessage
from zipfile import ZipInfo, ZIP_DEFLATED

from wheel.wheelfile import WheelFile


def _generate_metafile_content(headers: dict[str, str], payload=None):
    msg = EmailMessage()
    for name, value in headers.items():
        if isinstance(value, list):
            for value_part in value:
                msg[name] = value_part
        else:
            msg[name] = value
    if payload:
        msg.set_payload(payload)
    return msg


class ReproducibleWheelFile(WheelFile):
    def writestr(self, zip_info_or_filename: ZipInfo | str, *args, **kwargs):
        if isinstance(zip_info_or_filename, str):
            zip_info = ZipInfo(zip_info_or_filename)
        else:
            zip_info = zip_info_or_filename

        zip_info.compress_type = self.compression
        zip_info.external_attr = (0o774 | stat.S_IFREG) << 16
        zip_info.date_time = (1980, 1, 1, 0, 0, 0)
        zip_info.create_system = 3
        super().writestr(zip_info, *args, **kwargs)


def _write_wheel_file(filename: str, contents: dict[str, EmailMessage]):
    with ReproducibleWheelFile(filename, 'w') as wheel_file:
        for member_info, member_source in contents.items():
            if not isinstance(member_info, ZipInfo):
                member_info = ZipInfo(member_info)

            member_info.file_size = len(member_source)
            member_info.compress_type = ZIP_DEFLATED
            wheel_file.writestr(member_info, bytes(member_source))
    return filename


def _write_wheel(
        out_dir: str,
        name: str,
        version: str,
        tag: str,
        metadata: dict,
        description: str,
        contents: dict[str, bytes]
):
    wheel_name = f'{name}-{version}-{tag}.whl'
    dist_info = f'{name}-{version}.dist-info'
    return _write_wheel_file(os.path.join(out_dir, wheel_name), {
        **contents,
        f'{dist_info}/METADATA': _generate_metafile_content({
            'Metadata-Version': '2.1',
            'Name': name,
            'Version': version,
            **metadata,
        }, description),
        f'{dist_info}/WHEEL': _generate_metafile_content({
            'Wheel-Version': '1.0',
            'Generator': 'ziglang make_wheels.py',
            'Root-Is-Purelib': 'false',
            'Tag': tag,
        }),
    })
