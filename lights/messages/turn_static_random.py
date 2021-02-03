import random
from typing import Any, Dict

from lights.actions.change_color_action import ChangeColorAction
from lights.light_controller.light_controller import LightController
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnStaticRandom(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Mqtt.TOPIC + settings.Messages.TURN_STATIC_RANDOM
        self.light_controller = LightController()

    def _parse_payload(self, payload):
        self._logger.debug('Executing Turn Static Random message')
        color = payload.get(settings.Messages.COLOR, None)
        if color is None:
            color = tuple([random.randint(0, 255) for _ in range(3)])

        brightness = payload.get(settings.Messages.BRIGHTNESS, max(color))
        time_span = payload.get(settings.Messages.TIME_SPAN, 20)

        return color, brightness, time_span

    def execute(self, payload: Dict[str, Any]):
        self._logger.debug(f'Executing TurnStatic message with payload '
                           f'{payload}')
        color, brightness, time_span = self._parse_payload(payload)
        self.light_controller.state_on()
        action = ChangeColorAction(color, brightness, time_span)

        self.light_controller.add_action(action)
