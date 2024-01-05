import platform
import subprocess
import tempfile
from pathlib import Path
import os
import zipfile
import stat
from collections.abc import Sequence


def install_wheel(path: Path | str, name: str):
    os.system(f"pip3 install --force-reinstall --no-index --find-links  {path} {name}")


def verify_install(package: str, args: str = "--version"):
    output = subprocess.check_output(f"{package}{'.exe' if platform.system() == 'Windows' else ''} {args}", shell=True,
                                     text=True)
    assert output != ""

    output = subprocess.check_output(
        f"python{'.exe' if platform.system() == 'Windows' else ''} -m {package.replace('-', '_')} {args}", shell=True,
        text=True)
    assert output != ""


def verify_wheel_structure(wheel_path: Path | str, files_present: Sequence[tuple[str, int]], files_absent=None):
    class ZipFileWithPermissions(zipfile.ZipFile):
        def _extract_member(self, member, target_path, pwd):
            if not isinstance(member, zipfile.ZipInfo):
                member = self.getinfo(member)

            target_path = super()._extract_member(member, target_path, pwd)

            attr = member.external_attr >> 16
            if attr != 0:
                os.chmod(target_path, attr)
            return target_path

    if files_absent is None:
        files_absent = []

    with ZipFileWithPermissions(wheel_path, 'r') as zip_file:
        for file in files_absent:
            assert file not in zip_file.namelist()

        for file_info in files_present:
            file_name, expected_permissions = file_info
            assert file_name in zip_file.namelist()

            extracted_path = zip_file.extract(file_name, tempfile.mkdtemp())

            actual_permissions = stat.S_IMODE(os.stat(extracted_path).st_mode)
            if platform.system() != "Windows":
                assert actual_permissions == expected_permissions

            os.remove(extracted_path)
