from lights.errors.lights_exception import LightsException


class DeveloperException(LightsException):
    def __init__(self, message):
        super().__init__(message)
