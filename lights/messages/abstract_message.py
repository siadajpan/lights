import logging
from abc import ABC
from typing import Dict, Any

from lights.settings import settings


class AbstractMessage(ABC):
    def __init__(self):
        self.topic = settings.Mqtt.TOPIC
        self.payload = ''
        self._logger = logging.getLogger(self.__class__.__name__)

    def execute(self, payload: Dict[str, Any]):
        raise NotImplementedError()

    def __repr__(self):
        return f'Message with topic: {self.topic}, payload: {self.payload}'
