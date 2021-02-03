from lights.errors.lights_exception import LightsException


class IncorrectTopicException(LightsException):
    def __init__(self, message):
        super().__init__(message)
