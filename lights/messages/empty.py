from lights.light_controller.light_controller import LightController
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class Empty(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Messages.EMPTY

    def execute(self, *args, **kwargs):
        pass
