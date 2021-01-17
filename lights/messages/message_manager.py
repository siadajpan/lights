import logging
from typing import List

from lights.errors.incorrect_topic_exception import IncorrectTopicException
from lights.messages.abstract_message import AbstractMessage
from lights.messages.turn_off import TurnOff
from lights.messages.turn_slowly_static import TurnSlowlyStatic
from lights.messages.turn_static_color import TurnStaticColor
from lights.settings import settings

MESSAGES = [TurnOff(), TurnStaticColor(), TurnSlowlyStatic()]


class MessageManager:
    def __init__(self):
        self.messages: List[AbstractMessage] = MESSAGES
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_message(self, payload: str, topic=settings.Mqtt.TOPIC):
        self.logger.debug(f'Searching for message topic: {topic}, payload: {payload}')
        for message in self.messages:
            if message.topic != topic:
                continue

            self.logger.debug('Executing message')
            message.execute(payload)

        error_message = f'Received message not found. Expected messages: ' \
                        f'{[(message.topic, message.payload) for message in self.messages]}'
        self.logger.error(error_message)

        raise IncorrectTopicException(error_message)
