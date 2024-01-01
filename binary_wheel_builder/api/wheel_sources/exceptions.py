from binary_wheel_builder.api.meta import WheelPlatformIdentifier


class WheelSourceException(Exception):
    pass


class UnsupportedWheelPlatformException(WheelSourceException):
    def __init__(self, wheel_platform: WheelPlatformIdentifier, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.wheel_platform = wheel_platform


class SourceFileRequestFailed(WheelSourceException):
    pass
