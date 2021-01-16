import logging
from abc import ABC

from lights.settings import settings


class AbstractMessage(ABC):
    def __init__(self):
        self.topic = settings.Mqtt.TOPIC
        self.payload = ''
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute(self, *args, **kwargs):
        raise NotImplementedError()
