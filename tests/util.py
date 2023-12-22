import os
import subprocess
from pathlib import Path


def install_wheel(path: Path | str, name : str):
    os.system(f"pip3 install --force-reinstall --no-index --find-links  {path} {name}")


def verify_install(package: str, args: str = "--version"):
    #output = subprocess.check_output(f"{package} {args}", shell=True, text=True)
    #assert output != ""

    output = subprocess.check_output(f"python3 -m {package.replace('-','_')} {args}", shell=True, text=True)
    assert output != ""