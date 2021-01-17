import logging

import paho.mqtt.client as mqtt

from lights.errors.incorrect_payload_exception import IncorrectPayloadException
from lights.errors.incorrect_topic_exception import IncorrectTopicException
from lights.errors.lights_exception import LightsException
from lights.messages.message_manager import MessageManager
from lights.settings import settings


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(client_id="", clean_session=True, userdata=None,
                                  protocol=mqtt.MQTTv311, transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username=settings.Mqtt.USERNAME,
                                    password=settings.Mqtt.PASSWORD)
        self.message_manager = MessageManager()
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect(self):
        self.logger.info(f'MQTT client connecting to '
                         f'{settings.Mqtt.ADDRESS}:{settings.Mqtt.PORT}')
        self.client.connect(
            settings.Mqtt.ADDRESS, settings.Mqtt.PORT, 60)

    def loop_forever(self):
        self.logger.info('MQTT client looping start')
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info(f'MQTT connected')
        topic = settings.Mqtt.TOPIC + '#'
        self.logger.info(f'Subscribing to {topic}')
        self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        self.logger.info(f'Message received topic: '
                         f'{msg.topic}, payload: {msg.payload}')
        try:
            self.message_manager.execute_message(msg.payload, msg.topic)
        except LightsException as ex:
            self.client.publish(settings.Mqtt.ERROR_TOPIC, ex.message)
        except Exception as ex:
            self.client.publish(settings.Mqtt.ERROR_TOPIC, ex)
