binary-wheel-builder
===
[![PyPI version](https://badge.fury.io/py/binary_wheel_builder.svg)](https://pypi.org/project/binary_wheel_builder)
[![LICENSE](https://img.shields.io/github/license/timo-reymann/python-binary-wheel-builder)](https://github.com/timo-reymann/binary-wheel-builder/blob/main/LICENSE)
[![CircleCI](https://circleci.com/gh/timo-reymann/python-binary-wheel-builder.svg?style=shield)](https://app.circleci.com/pipelines/github/timo-reymann/python-binary-wheel-builder)
[![codecov](https://codecov.io/gh/timo-reymann/python-binary-wheel-builder/graph/badge.svg?token=LFBPaleiaO)](https://codecov.io/gh/timo-reymann/python-binary-wheel-builder)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=timo-reymann_python-binary-wheel-builder&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=timo-reymann_python-binary-wheel-builder)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=timo-reymann_python-binary-wheel-builder&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=timo-reymann_python-binary-wheel-builder)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=timo-reymann_python-binary-wheel-builder&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=timo-reymann_python-binary-wheel-builder)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=timo-reymann_python-binary-wheel-builder&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=timo-reymann_python-binary-wheel-builder)
[![Renovate](https://img.shields.io/badge/renovate-enabled-green?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNjkgMzY5Ij48Y2lyY2xlIGN4PSIxODkuOSIgY3k9IjE5MC4yIiByPSIxODQuNSIgZmlsbD0iI2ZmZTQyZSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTUgLTYpIi8+PHBhdGggZmlsbD0iIzhiYjViNSIgZD0iTTI1MSAyNTZsLTM4LTM4YTE3IDE3IDAgMDEwLTI0bDU2LTU2YzItMiAyLTYgMC03bC0yMC0yMWE1IDUgMCAwMC03IDBsLTEzIDEyLTktOCAxMy0xM2ExNyAxNyAwIDAxMjQgMGwyMSAyMWM3IDcgNyAxNyAwIDI0bC01NiA1N2E1IDUgMCAwMDAgN2wzOCAzOHoiLz48cGF0aCBmaWxsPSIjZDk1NjEyIiBkPSJNMzAwIDI4OGwtOCA4Yy00IDQtMTEgNC0xNiAwbC00Ni00NmMtNS01LTUtMTIgMC0xNmw4LThjNC00IDExLTQgMTUgMGw0NyA0N2M0IDQgNCAxMSAwIDE1eiIvPjxwYXRoIGZpbGw9IiMyNGJmYmUiIGQ9Ik04MSAxODVsMTgtMTggMTggMTgtMTggMTh6Ii8+PHBhdGggZmlsbD0iIzI1YzRjMyIgZD0iTTIyMCAxMDBsMjMgMjNjNCA0IDQgMTEgMCAxNkwxNDIgMjQwYy00IDQtMTEgNC0xNSAwbC0yNC0yNGMtNC00LTQtMTEgMC0xNWwxMDEtMTAxYzUtNSAxMi01IDE2IDB6Ii8+PHBhdGggZmlsbD0iIzFkZGVkZCIgZD0iTTk5IDE2N2wxOC0xOCAxOCAxOC0xOCAxOHoiLz48cGF0aCBmaWxsPSIjMDBhZmIzIiBkPSJNMjMwIDExMGwxMyAxM2M0IDQgNCAxMSAwIDE2TDE0MiAyNDBjLTQgNC0xMSA0LTE1IDBsLTEzLTEzYzQgNCAxMSA0IDE1IDBsMTAxLTEwMWM1LTUgNS0xMSAwLTE2eiIvPjxwYXRoIGZpbGw9IiMyNGJmYmUiIGQ9Ik0xMTYgMTQ5bDE4LTE4IDE4IDE4LTE4IDE4eiIvPjxwYXRoIGZpbGw9IiMxZGRlZGQiIGQ9Ik0xMzQgMTMxbDE4LTE4IDE4IDE4LTE4IDE4eiIvPjxwYXRoIGZpbGw9IiMxYmNmY2UiIGQ9Ik0xNTIgMTEzbDE4LTE4IDE4IDE4LTE4IDE4eiIvPjxwYXRoIGZpbGw9IiMyNGJmYmUiIGQ9Ik0xNzAgOTVsMTgtMTggMTggMTgtMTggMTh6Ii8+PHBhdGggZmlsbD0iIzFiY2ZjZSIgZD0iTTYzIDE2N2wxOC0xOCAxOCAxOC0xOCAxOHpNOTggMTMxbDE4LTE4IDE4IDE4LTE4IDE4eiIvPjxwYXRoIGZpbGw9IiMzNGVkZWIiIGQ9Ik0xMzQgOTVsMTgtMTggMTggMTgtMTggMTh6Ii8+PHBhdGggZmlsbD0iIzFiY2ZjZSIgZD0iTTE1MyA3OGwxOC0xOCAxOCAxOC0xOCAxOHoiLz48cGF0aCBmaWxsPSIjMzRlZGViIiBkPSJNODAgMTEzbDE4LTE3IDE4IDE3LTE4IDE4ek0xMzUgNjBsMTgtMTggMTggMTgtMTggMTh6Ii8+PHBhdGggZmlsbD0iIzk4ZWRlYiIgZD0iTTI3IDEzMWwxOC0xOCAxOCAxOC0xOCAxOHoiLz48cGF0aCBmaWxsPSIjYjUzZTAyIiBkPSJNMjg1IDI1OGw3IDdjNCA0IDQgMTEgMCAxNWwtOCA4Yy00IDQtMTEgNC0xNiAwbC02LTdjNCA1IDExIDUgMTUgMGw4LTdjNC01IDQtMTIgMC0xNnoiLz48cGF0aCBmaWxsPSIjOThlZGViIiBkPSJNODEgNzhsMTgtMTggMTggMTgtMTggMTh6Ii8+PHBhdGggZmlsbD0iIzAwYTNhMiIgZD0iTTIzNSAxMTVsOCA4YzQgNCA0IDExIDAgMTZMMTQyIDI0MGMtNCA0LTExIDQtMTUgMGwtOS05YzUgNSAxMiA1IDE2IDBsMTAxLTEwMWM0LTQgNC0xMSAwLTE1eiIvPjxwYXRoIGZpbGw9IiMzOWQ5ZDgiIGQ9Ik0yMjggMTA4bC04LThjLTQtNS0xMS01LTE2IDBMMTAzIDIwMWMtNCA0LTQgMTEgMCAxNWw4IDhjLTQtNC00LTExIDAtMTVsMTAxLTEwMWM1LTQgMTItNCAxNiAweiIvPjxwYXRoIGZpbGw9IiNhMzM5MDQiIGQ9Ik0yOTEgMjY0bDggOGM0IDQgNCAxMSAwIDE2bC04IDdjLTQgNS0xMSA1LTE1IDBsLTktOGM1IDUgMTIgNSAxNiAwbDgtOGM0LTQgNC0xMSAwLTE1eiIvPjxwYXRoIGZpbGw9IiNlYjZlMmQiIGQ9Ik0yNjAgMjMzbC00LTRjLTYtNi0xNy02LTIzIDAtNyA3LTcgMTcgMCAyNGw0IDRjLTQtNS00LTExIDAtMTZsOC04YzQtNCAxMS00IDE1IDB6Ii8+PHBhdGggZmlsbD0iIzEzYWNiZCIgZD0iTTEzNCAyNDhjLTQgMC04LTItMTEtNWwtMjMtMjNhMTYgMTYgMCAwMTAtMjNMMjAxIDk2YTE2IDE2IDAgMDEyMiAwbDI0IDI0YzYgNiA2IDE2IDAgMjJMMTQ2IDI0M2MtMyAzLTcgNS0xMiA1em03OC0xNDdsLTQgMi0xMDEgMTAxYTYgNiAwIDAwMCA5bDIzIDIzYTYgNiAwIDAwOSAwbDEwMS0xMDFhNiA2IDAgMDAwLTlsLTI0LTIzLTQtMnoiLz48cGF0aCBmaWxsPSIjYmY0NDA0IiBkPSJNMjg0IDMwNGMtNCAwLTgtMS0xMS00bC00Ny00N2MtNi02LTYtMTYgMC0yMmw4LThjNi02IDE2LTYgMjIgMGw0NyA0NmM2IDcgNiAxNyAwIDIzbC04IDhjLTMgMy03IDQtMTEgNHptLTM5LTc2Yy0xIDAtMyAwLTQgMmwtOCA3Yy0yIDMtMiA3IDAgOWw0NyA0N2E2IDYgMCAwMDkgMGw3LThjMy0yIDMtNiAwLTlsLTQ2LTQ2Yy0yLTItMy0yLTUtMnoiLz48L3N2Zz4=)](https://renovatebot.com)

<p align="center">
	<img width="300" src="https://raw.githubusercontent.com/timo-reymann/python-binary-wheel-builder/main/.github/images/logo.png">
    <br />
    Build deterministic python wheels to distribute CLI tools (third party or your own with python and make them easily usable using python code.
</p>

## Features

- deterministic wheel file output
- Use with Python Code or as CLI
- [Prebuilt data sources](https://timo-reymann.github.io/binary_wheel_builder.api.wheel_sources.html) for your binaries
- Ready to release and ship your binaries
- Wrapper for cli calls inside Python
- Exposes wheel as module entrypoint (`python -m your_cli`) and adds to path (`your-cli`)

## Requirements

- Python 3.8+ for host running wheel build
- For target host every 3.x should work

## Installation

### ... with pip

```sh
# with CLI dependencies
pip install binary_wheel_builder[cli]

# as SDK
pip install binary_wheel_builder
```

### ... with pipx

````sh
pipx install binary_wheel_builder[cli]
````

## Usage

### Build with CLI

1. Create your config file e. g. `my-cli-wheel.yaml`:
   ```yaml
   package: my_cli
   executable: my-cli-bin
   name: my-cli
   version: 0.0.1
   summary: My CLI provides nice and clean functionality on the terminal
   description: !FileContent README.md
   license: MIT
   requires_python: ">=3.8"
   classifier:
      - "License :: OSI Approved :: MIT License"
      # Check https://pypi.org/classifiers/ for all available
   project_urls:
      # Set project urls as you like
      "Homepage": "https://github.com/my-org/my-cli"
      "Source Code": "https://github.com/my-org/my-cli,git"
      "Bug Tracker": "https://github.com/my-org/my-cli/issues"
   source: !WheelSource
     # Fetch binary from GitHub releases
     implementation: binary_wheel_builder.api.wheel_sources.GithubReleaseBinarySource
     project_slug: my-org/my-cli
     version: "0.0.1"
     tag_prefix: "" # e.g. set to v when your tag is vX.Y.Z
    # Path of the binary relative to your package root
     binary_path: my_cli/my-cli-bin
     # Download file name based on platform the wheel is built for
     asset_name_mapping:
       !WellknownPlatform MAC_SILICON: "mycli-darwin-arm64"
       !WellknownPlatform MAC_INTEL: "mycli-darwin-amd64"
       !WellknownPlatform LINUX_GENERIC_x86_64: "my-cli-linux-amd64"
       !WellKnownPlatform LINUX_GENERIC_aarch64: "my-cli-linux-arm"
     # Supported platforms by the wheel
     platforms:
       - !WellknownPlatform MAC_INTEL
       - !WellknownPlatform MAC_SILICON
       - !WellknownPlatform LINUX_GENERIC_x86_64
       - !WellKnownPlatform LINUX_GENERIC_aarch64
   ```
2. Build your wheel for all platforms
   ```shell
   binary-wheel-builder --wheel-spec my-cli-wheel.yaml
   ```
3. Upload your wheel files using [twine](https://twine.readthedocs.io/en/stable/):
   ```sh
   twine upload -r pypi dist/*
   ```
4. Enjoy and consume your CLI as a package

### Build with Python code

If you prefer to write Python Code you use almost the same structure:

````python
from pathlib import Path

from binary_wheel_builder.api import build_wheel, Wheel, well_known_platforms
from binary_wheel_builder.api.wheel_sources import GithubReleaseBinarySource


# Add a custom github release source
class MyCliGithubReleaseSource(GithubReleaseBinarySource):
    def __init__(self, version: str):
        super().__init__(
            "my-org/my-repo",
            version,
            {
                well_known_platforms.MAC_SILICON: "mycli-darwin-arm64",
                well_known_platforms.MAC_INTEL: "mycli-darwin-amd64",
                well_known_platforms.LINUX_GENERIC_x86_64: "my-cli-linux-amd64",
                well_known_platforms.LINUX_GENERIC_aarch64: "my-cli-linux-arm",
            },
            "my_cli/my-cli-bin"
        )


dist_folder = Path("dist")

print("Built wheels:")
for result in build_wheel(
        Wheel(
            package="my_cli",
            executable="my-cli-bin",
            name="my-cli",
            version="0.0.1",
            summary='My CLI provides nice and clean functionality on the terminal',
            license='MIT',
            requires_python=">=3.9",
            classifier=[
                'License :: OSI Approved :: MIT License',
                # Check https://pypi.org/classifiers/ for all available
            ],
            project_urls={
                'Homepage': 'https://github.com/my-org/my-cli',
                'Source Code': 'https://github.com/my-org/my-cli,git',
                'Bug Tracker': 'https://github.com/my-org/my-cli/issues',
            },
            source=MyCliGithubReleaseSource("0.0.1"),
            platforms=[
                well_known_platforms.MAC_INTEL,
                well_known_platforms.MAC_SILICON,
                well_known_platforms.LINUX_GENERIC_x86_64,
                well_known_platforms.LINUX_GENERIC_aarch64
            ]
        ),
        dist_folder
):
    print(f" > {result.file_path} [{result.checksum}]")
````

Afterwards upload with twine:
Upload your wheel files using [twine](https://twine.readthedocs.io/en/stable/):

```sh
twine upload -r pypi dist/*
```

### Using the generated wheel

#### With python module call

```sh
python -m my_cli
```

#### Using wrapper in path

````sh
my-cli
````

#### Using in Python code using exec utils

```python
import subprocess

from my_cli import exec

# Run process and prefix stdout and stderr
exec.exec_with_templated_output(["--help"])

# Create a subprocess, specifying how to handle stdout, stderr
exec.create_subprocess(["--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Perform command with suppressed output and return finished proces instance,
# on that one can also check if the call was successfully
exec.exec_silently(["--version"])
```

## Motivation

Sometimes managing CLI dependencies for tooling etc. can become quite a pain.

Also sometimes there are just so many options to distribute binaries, but Python is preinstalled on almost any nix
machine.
This opens great possibilities with using pip(x) to install dependencies or even reuse standalone CLI applications as
regular dependency in your code.

## Documentation

- [Library documentation](https://timo-reymann.github.io/python-binary-wheel-builder/)

## Contributing

I love your input! I want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the configuration
- Submitting a fix
- Proposing new features
- Becoming a maintainer

To get started please read the [Contribution Guidelines](./CONTRIBUTING.md).

## Development

### Requirements

- Python 3.8+
- Poetry

### Test

### Integration Tests

```sh
poetry run pytest integration_tests/
```

### Unit Tests

```sh
poetry run pytest binary_wheel_builder/
```

### Build

````sh
poetry install
````

### Alternatives

- Using platform native package management
- curl'ing dependencies


