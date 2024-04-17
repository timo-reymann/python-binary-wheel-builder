"""
Contains the well known platforms for python wheel one might want to target to simplify usage
"""
from binary_wheel_builder.api.meta import WheelPlatformIdentifier

WINDOWS_i386 = WheelPlatformIdentifier(platform="win32")
WINDOWS_x86_64 = WheelPlatformIdentifier(platform="win_amd64")
MAC_INTEL = WheelPlatformIdentifier(platform="macosx_10_9_x86_64")
MAC_SILICON = WheelPlatformIdentifier(platform="macosx_11_0_arm64")
LINUX_GENERIC_x86_64 = WheelPlatformIdentifier(platform="manylinux_2_12_x86_64.manylinux2010_x86_64")
LINUX_GENERIC_x84_64 = LINUX_GENERIC_x86_64  # backwards compatibility (issue #12)
LINUX_GENERIC_i386 = WheelPlatformIdentifier(platform="manylinux_2_12_i686.manylinux2010_i686")
LINUX_GENERIC_armv7a = WheelPlatformIdentifier(platform="manylinux_2_17_armv7l.manylinux2014_armv7l")
LINUX_GENERIC_aarch64 = WheelPlatformIdentifier(platform="manylinux_2_17_aarch64.manylinux2014_aarch64")
