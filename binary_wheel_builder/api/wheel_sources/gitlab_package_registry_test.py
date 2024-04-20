from unittest import mock
from unittest.mock import MagicMock
from urllib.error import HTTPError

import pytest

from binary_wheel_builder.api import well_known_platforms
from binary_wheel_builder.api.wheel_sources.exceptions import WheelSourceException
from binary_wheel_builder.api.wheel_sources.gitlab_package_registry import GitlabGenericPackageRegistrySource


@pytest.mark.parametrize(
    [
        "tag_prefix",
        "status_code",
    ], [
        ["v", 404],
        ["", 404]
    ]
)
def test_gitlab_package_registry_binary_wheel_source(tag_prefix: str, status_code: int):
    request_fail = True if status_code < 200 or status_code > 300 else False
    with mock.patch(
            "urllib.request.urlopen",
            return_value=MagicMock(return_value=None),
            side_effect=HTTPError(
                'http://example.com', status_code, 'status', {},
                None
                ) if request_fail else None
            ) as urlopen_mock:
        source = GitlabGenericPackageRegistrySource(
            {
                well_known_platforms.LINUX_GENERIC_i386: "foo-bar"
            },
            "foo-bar",
            "org/project",
            "0.0.1",
            "foo-bar"
        )

        if request_fail:
            with pytest.raises(WheelSourceException):
                source.generate_fileset(well_known_platforms.LINUX_GENERIC_i386)
        else:
            source.generate_fileset(well_known_platforms.LINUX_GENERIC_i386)
            urlopen_mock.read.assert_called_once()

        urlopen_mock.assert_called_once()
