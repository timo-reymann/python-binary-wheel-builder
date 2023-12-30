import stat
from zipfile import ZipInfo, ZIP_DEFLATED

from wheel.wheelfile import WheelFile

from binary_wheel_builder.api.meta import WheelFileEntry


class ReproducibleWheelFile(WheelFile):
    def write_content_file(self, wheel_entry: WheelFileEntry) -> None:
        zip_info = ZipInfo(wheel_entry.path)
        zip_info.external_attr = (wheel_entry.permissions | stat.S_IFREG) << 16
        zip_info.file_size = len(wheel_entry.content)
        zip_info.create_system = 3
        self.writestr(zip_info, data=wheel_entry.content)

    def writestr(self, zip_info: ZipInfo | str, *args, **kwargs):
        if isinstance(zip_info, str):
            zip_info = ZipInfo(zip_info)
            zip_info.external_attr = (0o644 | stat.S_IFREG) << 16
        zip_info.compress_type = ZIP_DEFLATED
        zip_info.date_time = (1980, 1, 1, 0, 0, 0)
        zip_info.create_system = 3
        super().writestr(zip_info, *args, **kwargs)
