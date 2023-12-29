#!/usr/bin/env python3
import os
from pathlib import Path

from pydantic import TypeAdapter
from binary_wheel_builder import Wheel
import json

schema = TypeAdapter(Wheel).json_schema()
script_path = os.path.abspath(__file__)
folder_name = os.path.basename(os.path.dirname(script_path))

with Path(folder_name, "..", "wheel.schema.json").open("w") as f:
    json.dump(schema, f, indent=3)
