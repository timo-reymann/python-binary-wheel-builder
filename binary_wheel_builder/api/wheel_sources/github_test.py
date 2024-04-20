from unittest import mock
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError

import pytest

from binary_wheel_builder.api import well_known_platforms
from binary_wheel_builder.api.wheel_sources import GithubReleaseBinarySource
from binary_wheel_builder.api.wheel_sources.exceptions import WheelSourceException


@pytest.mark.parametrize([
    "tag_prefix",
    "status_code",
], [
    ["v", 404],
    ["", 404]
])
def test_github_release_binary_wheel_source(tag_prefix: str, status_code: int):
    request_fail = True if status_code < 200 or status_code > 300 else False
    with mock.patch("urllib.request.urlopen",
                    return_value=MagicMock(return_value=None),
                    side_effect=HTTPError('http://example.com', status_code, 'status', {},
                                          None) if request_fail else None) as urlopen_mock:
        source = GithubReleaseBinarySource(
            "org/project",
            "0.0.1", {
                well_known_platforms.LINUX_GENERIC_i386: "foo-bar"
            },
            "foo-bar",
            tag_prefix
        )

        if request_fail:
            with pytest.raises(WheelSourceException):
                source.generate_fileset(well_known_platforms.LINUX_GENERIC_i386)
        else:
            source.generate_fileset(well_known_platforms.LINUX_GENERIC_i386)
            urlopen_mock.read.assert_called_once()

        urlopen_mock.assert_called_once()
