from pathlib import Path

import yaml
from pydantic import ValidationError

from binary_wheel_builder import Wheel
from binary_wheel_builder.cli.yaml import load_file


def load_wheel_spec_from_yaml(file_path: Path):
    data = load_file(file_path)
    if data is None:
        raise ValueError("Config file can not be empty")
    data = {k: v for k, v in data.items() if k[0] != "."}

    try:
        return Wheel(**data)
    except ValidationError as e:
        raise yaml.YAMLError(f"Failed to deserialize to wheel: {str(e)}", e)
