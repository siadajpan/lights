from typing import Tuple

from lights.errors.incorrect_payload import IncorrectPayloadException
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnStaticColor(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Mqtt.TOPIC + settings.Messages.TURN_STATIC
        self.light_controller = LightController()

    def execute(self, *args, **kwargs):
        self.logger.debug('Checking if color is correctly formatted')
        color = utils.check_color_message(args[0])
        self.logger.debug('Color has correct format')
        self.light_controller.turn_static_color(color)
