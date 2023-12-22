import os

import unittest
from cli_wheel_builder.cli.main import main


class CliTest(unittest.TestCase):
    def test_cli(self):
        script_path = os.path.abspath(__file__)
        folder_name = os.path.basename(os.path.dirname(script_path))

        main([
            "--wheel-spec",
            f"{folder_name}/testdata/wheel.yaml",
            "--dist-folder",
            "/tmp/dist"
        ])
