class LightsException(BaseException):
    def __init__(self, message):
        self.message = message
