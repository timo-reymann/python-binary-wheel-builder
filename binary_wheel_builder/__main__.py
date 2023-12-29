from pydantic import TypeAdapter

from binary_wheel_builder import Wheel
from binary_wheel_builder.cli.main import main

if __name__ == "__main__":
    schema = TypeAdapter(Wheel).json_schema()
    main()
