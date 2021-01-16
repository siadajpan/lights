from typing import Tuple

from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnStaticColor(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.payload = settings.Messages.TURN_STATIC
        self.light_controller = LightController()

    def execute(self, *args, **kwargs):
        self.logger.debug('Executing turn_static message')
        color = kwargs.get(settings.Messages.COLOR, None)
        if color is None:
            error_msg = 'Executing Turn static color without ' \
                        'color value in payload'
            self.logger.error(error_msg)
            return False

        color = eval(color)
        self.logger.debug('Checking if color is correctly formatted')
        utils.check_color_message(color)
        self.logger.debug('Color has correct format')
        self.light_controller.turn_static_color(color)
