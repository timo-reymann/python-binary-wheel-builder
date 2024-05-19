"""
Contains a curated list of supported wheel sources
"""
from binary_wheel_builder.api.wheel_sources.github import GithubReleaseBinarySource
from binary_wheel_builder.api.wheel_sources.static import StaticLocalWheelSource
from binary_wheel_builder.api.wheel_sources.platform_based_file import PlatformBasedFileSource
import binary_wheel_builder.api.wheel_sources.exceptions