from lights.errors.lights_exception import LightsException


class IncorrectTopicException(BaseException):
    def __init__(self, message):
        self.message = message
