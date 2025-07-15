import io
from unittest import mock
from unittest.mock import MagicMock
from urllib.error import HTTPError

import pytest

from binary_wheel_builder.api import well_known_platforms
from binary_wheel_builder.api.wheel_sources import GithubReleaseBinarySource
from binary_wheel_builder.api.wheel_sources.exceptions import WheelSourceException


@pytest.mark.parametrize(
    [
        "tag_prefix",
        "status_code",
    ],
    [
        ["v", 404],
        ["", 404],
    ],
)
def test_github_release_binary_wheel_source(tag_prefix: str, status_code: int):
    with mock.patch(
        "urllib.request.urlopen",
        return_value=MagicMock(read=io.BytesIO(b"")),
        side_effect=HTTPError("http://example.com", status_code, "status", {}, None)
    ) as urlopen_mock:
        source = GithubReleaseBinarySource(
            "org/project",
            "0.0.1",
            {
                well_known_platforms.LINUX_GENERIC_x86_64: "foo-bar-$version.tar.gz",
            },
            "foo-bar",
            tag_prefix,
        )

        with pytest.raises(WheelSourceException):
            source.generate_fileset(well_known_platforms.LINUX_GENERIC_x86_64)
        urlopen_mock.assert_called_once()
        full_url = urlopen_mock.call_args[0][0].full_url
        assert full_url == f"https://github.com/org/project/releases/download/{tag_prefix}0.0.1/foo-bar-0.0.1.tar.gz"
