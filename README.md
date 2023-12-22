Proof of concept - Ship CLI tools using python wheels
==

Proof of concept to create a CLI binary as wheel in a reusable manner.

This would allow:

- easy distribution of CLI tools with managed version
- Installation via pip/pix or via package manager as regular dependency

## Setup

1. Install dependencies with poetry:
   ```sh
   poetry install
   ```
   (or just do `pip install wheels pytest` in case you dont have poetry installed)
2. Checkout binary_wheel_bundler/ and tests/

## Features

- Meta data is defined with auto complete dataclass
- Idempotent zip files with resetted timestamps on file content
- Checksum calc for output
- Simple to use API
- Supports basically every binary
- Extendable Source file generation (fetch from remote, fs, compile etc)
- Generated util package for easy getting started
  ```python
  # lets take for example buf package
  from buf.exec import exec_silently, exec_with_templated_output
    
  process = exec_silently(["--help"])
  print(process.returncode)
    
  result = exec_with_templated_output(["--help"])
  print(result.exit_code)
  ```
- Add binary to path so one can call it by binary name and it is managed by pip
- CLI to define wheel config as YAML, without having to touch python
  ```sh
  poetry run cli-wheel-builder --wheel-spec tests/testdata/wheel.yaml
  ```

## Limitations

- Files are loaded completely in-memory, this should not be a problem as long as you are not using a too huge binary.
  With a certain size RAM becomes the limit.
  You should not package any files that are that large, so thats a more theoretical limitation.
- Package can not be nested (for now) - for simplicity reasons

## Run it

- ```python3 -m pytest .```
- Check tests, extend try to install a wheel