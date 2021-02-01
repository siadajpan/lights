import random
from typing import Any, Dict

from lights.actions.set_color_action import SetColor
from lights.light_controller.light_controller import LightController
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnStaticRandom(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Mqtt.TOPIC + settings.Messages.TURN_STATIC_RANDOM
        self.light_controller = LightController()

    def execute(self, payload: Dict[str, Any]):
        self.logger.debug(f'Executing TurnStatic message with payload '
                          f'{payload}')
        action = SetColor()
        random_color = tuple([random.randint(0, 255) for _ in range(3)])
        action.set_color(random_color)
        action.set_brightness(random.randint(0, 255))

        self.light_controller.add_action(action)
