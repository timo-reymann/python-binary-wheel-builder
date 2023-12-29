"""
Contains the well known platforms for python wheel one might want to target to simplify usage
"""
from binary_wheel_builder.api._meta import WheelPlatformIdentifier

WINDOWS_i386 = WheelPlatformIdentifier("win32")
WINDOWS_x86_64 = WheelPlatformIdentifier("win_amd64")
MAC_INTEL = WheelPlatformIdentifier("macosx_10_9_x86_64")
MAC_SILICONE = WheelPlatformIdentifier("macosx_11_0_arm64")
LINUX_GENERIC_x84_64 = WheelPlatformIdentifier("manylinux_2_12_x86_64.manylinux2010_x86_64")
LINUX_GENERIC_i386 = WheelPlatformIdentifier("manylinux_2_12_i686.manylinux2010_i686")
LINUX_GENERIC_armv7a = WheelPlatformIdentifier("manylinux_2_17_armv7l.manylinux2014_armv7l")
LINUX_GENERIC_aarch64 = WheelPlatformIdentifier("manylinux_2_17_aarch64.manylinux2014_aarch64")
