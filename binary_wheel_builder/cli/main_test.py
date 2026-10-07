import os
from pathlib import Path

import pytest

from binary_wheel_builder.cli.main import _safe_path


def test_safe_path_resolves_relative_path_inside_cwd():
    assert _safe_path("dist") == Path(os.path.realpath("dist"))


def test_safe_path_rejects_relative_traversal():
    with pytest.raises(ValueError):
        _safe_path("../../definitely-outside")


def test_safe_path_allows_absolute_path(tmp_path):
    assert _safe_path(str(tmp_path)) == Path(os.path.realpath(str(tmp_path)))


def test_safe_path_allows_absolute_path_outside_cwd():
    assert _safe_path("/tmp/dist") == Path(os.path.realpath("/tmp/dist"))
