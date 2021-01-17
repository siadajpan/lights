from lights.errors.lights_exception import LightsException


class IncorrectPayloadException(BaseException):
    def __init__(self, message):
        self.message = message
