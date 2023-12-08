Proof of concept - Ship CLI tools using python wheels
==

Proof of concept to create a CLI binary as wheel in a reusable manner.

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
- Supports bascially every binary
- Extendable Source file generation (fetch from remote, fs, compile etc)

## Limitations

- Files are loaded completely in-memory, this should not be a problem as long as you are not using a too huge binary.
  With a certain size RAM becomes the limit.
  You should not package any files that are that large, so thats a more theoretical limitation.
- For now only single binaries are supported, irl use cases might include lib folders, dll/so files etc

## Run it

- ```python3 -m pytest .```
- Check tests, extend try to install a wheel