import logging
from queue import Queue
from threading import Thread
from typing import List, Callable

from lights.errors.incorrect_topic_exception import IncorrectTopicException
from lights.errors.lights_exception import LightsException
from lights.messages.abstract_message import AbstractMessage
from lights.messages.empty import Empty
from lights.messages.turn_off import TurnOff
from lights.messages.turn_slowly_static import TurnSlowlyStatic
from lights.messages.turn_static import TurnStatic
from lights.settings import settings
import paho.mqtt.client as mqtt

MESSAGES = [TurnOff(), TurnStatic(), TurnSlowlyStatic(), Empty()]


class MessageManager(Thread):
    def __init__(self, message_queue: Queue, publish_method: Callable):
        super().__init__()
        self.messages: List[AbstractMessage] = MESSAGES
        self.logger = logging.getLogger(self.__class__.__name__)
        self._topic_registered = [message.topic for message in self.messages]
        self.message_queue = message_queue
        self._publish_method = publish_method
        self._stop = False

    def publish(self, topic, payload):
        self._publish_method(topic, payload)

    def execute_message(self, payload: str, topic=settings.Mqtt.TOPIC):
        message = self.check_message(topic)
        try:
            message.execute(payload)
        except Exception as ex:
            self.logger.error(f'Error raised during execution of message. '
                              f'Exception: {ex}')
            raise ex

    def check_message(self, topic) -> AbstractMessage:
        self.logger.debug(f'Searching for message topic: {topic}')
        if topic in self._topic_registered:
            return self.messages[self._topic_registered.index(topic)]

        error_message = \
            f'Received message not registered. Registered topics: ' \
            f'{[message.topic for message in self.messages]} got: {topic}'

        self.logger.error(error_message)

        raise IncorrectTopicException(error_message)

    def run(self) -> None:
        while not self._stop:
            message: mqtt.MQTTMessage = self.message_queue.get()
            try:
                self.execute_message(message.payload, message.topic)
            except LightsException as ex:
                self.publish(settings.Mqtt.ERROR_TOPIC, ex.message)
            except Exception as ex:
                self.publish(settings.Mqtt.ERROR_TOPIC, ex)

    def stop(self):
        self._stop = True
        self.message_queue.put(Empty())
