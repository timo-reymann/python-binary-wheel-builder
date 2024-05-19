"""
Exceptions that can be thrown when working with sources
"""
from binary_wheel_builder.api.meta import WheelPlatformIdentifier


class WheelSourceException(Exception):
    pass


class UnsupportedWheelPlatformException(WheelSourceException):
    """Is raised when the request wheel platform is not supported by the source"""
    def __init__(self, wheel_platform: WheelPlatformIdentifier, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.wheel_platform = wheel_platform


class SourceFileRequestFailed(WheelSourceException):
    """Is raised when loading the source for the wheel is failing"""
    pass
