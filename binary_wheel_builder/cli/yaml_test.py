import io
import os
import tempfile
from pathlib import Path

import pytest
import yaml.constructor

from binary_wheel_builder import WheelPlatformIdentifier
from binary_wheel_builder.api import well_known_platforms
from binary_wheel_builder.api.wheel_sources import GithubReleaseBinarySource
from binary_wheel_builder.cli.yaml import load_stream


def _parse_string(content: str):
    return load_stream(io.StringIO(content), Path("dummy.yaml"))


def test_tag_well_known_platform_valid():
    parsed = _parse_string("""\
platform: !WellknownPlatform MAC_SILICON
    """)
    assert 'platform' in parsed
    assert parsed['platform'] == well_known_platforms.MAC_SILICON


def test_tag_well_known_platform_invalid():
    with pytest.raises(yaml.constructor.ConstructorError) as exc:
        _parse_string("""\
        platform: !WellknownPlatform NON_EXISTENT
            """)
    assert ('could not determine well known platform with name NON_EXISTENT\n'
            '  in "<file>", line 1, column 19') == str(exc.value)


def test_tag_file_content_valid():
    file_content = "File content"
    with tempfile.NamedTemporaryFile(mode="w") as fp:
        fp.write(file_content)
        fp.flush()

        parsed = _parse_string(f"""\
        content: !FileContent {fp.name}
        """)
        assert 'content' in parsed
        assert parsed['content'] == "File content"


def test_tag_file_content_not_found():
    with pytest.raises(yaml.constructor.ConstructorError) as exc:
        _parse_string("""\
                content: !FileContent file.txt
                """)
    assert 'file.txt does not resolve to a file\n  in "<file>", line 1, column 26' == str(exc.value)


def test_tag_platform_identifier():
    parsed = _parse_string('''\
    !WheelPlatform
        platform: manylinux_3_0_i686
        python_tag: cpy3
    ''')
    assert parsed is not None
    assert isinstance(parsed, WheelPlatformIdentifier)
    assert "manylinux_3_0_i686" == parsed.platform
    assert "cpy3" == parsed.python_tag


def test_tag_platform_identifier_unknown_field():
    with pytest.raises(yaml.constructor.ConstructorError) as exc:
        _parse_string('''\
        !WheelPlatform
            platform: manylinux_3_0_i686
            python_tag: cpy3
            tag: asfd
        ''')
    assert 'Unsupported argument tag with value \'asfd\'\n  in "<file>", line 1, column 9' == str(exc.value)


def test_tag_wheel_source():
    content = _parse_string('''\
    !WheelSource
        implementation: binary_wheel_builder.api.wheel_sources.GithubReleaseBinarySource
        project_slug: timo-reymann/deterministic-zip
        version: "2.1.0"
        tag_prefix: ""
        binary_path: deterministic_zip/deterministic-zip
        asset_name_mapping: {}
    ''')
    assert content is not None
    assert isinstance(content, GithubReleaseBinarySource)


def test_tag_wheel_source_unknown():
    with pytest.raises(yaml.constructor.ConstructorError) as exc:
        _parse_string('''\
        !WheelSource
            implementation: unknownImplementation.blub
        ''')
    assert ("Wheel source implementation for tag '!WheelSource' could not be "
            'instantiated\n'
            '  in "<file>", line 1, column 9') == str(exc.value)


def test_tag_wheel_source_empty():
    with pytest.raises(yaml.constructor.ConstructorError) as exc:
        _parse_string('''\
        !WheelSource
            implementation: ""
        ''')
    assert ("No wheel source implementation specified in tag '!WheelSource'\n"
            '  in "<file>", line 1, column 9') == str(exc.value)


def test_tag_env_var_exists():
    val = os.environ['FOO'] = 'bar'
    _parse_string('''\
    !Env FOO
    ''')
    assert "bar" == val


def test_tag_env_var_not_set():
    with pytest.raises(yaml.constructor.ConstructorError) as exc:
        _parse_string('''\
        !Env FOO123
        ''')
    assert 'Environment variable FOO123 not set\n  in "<file>", line 1, column 9' == str(exc.value)
