from lights.errors.lights_exception import LightsException


class DeveloperException(BaseException):
    def __init__(self, message):
        self.message = message
