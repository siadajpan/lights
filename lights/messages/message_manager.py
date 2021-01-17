import logging
from typing import List

from lights.errors.incorrect_topic_exception import IncorrectTopicException
from lights.messages.abstract_message import AbstractMessage
from lights.messages.turn_off import TurnOff
from lights.messages.turn_slowly_static import TurnSlowlyStatic
from lights.messages.turn_static import TurnStatic
from lights.settings import settings

MESSAGES = [TurnOff(), TurnStatic(), TurnSlowlyStatic()]


class MessageManager:
    def __init__(self):
        self.messages: List[AbstractMessage] = MESSAGES
        self.logger = logging.getLogger(self.__class__.__name__)
        self._topic_registered = [message.topic for message in self.messages]

    def execute_message(self, payload: str, topic=settings.Mqtt.TOPIC):
        message = self.check_message(topic)
        message.execute(payload)

    def check_message(self, topic) -> AbstractMessage:
        self.logger.debug(f'Searching for message topic: {topic}')
        if topic in self._topic_registered:
            return self.messages[self._topic_registered.index(topic)]

        error_message = \
            f'Received message not registered. Registered topics: ' \
            f'{[message.topic for message in self.messages]} got: {topic}'

        self.logger.error(error_message)

        raise IncorrectTopicException(error_message)
