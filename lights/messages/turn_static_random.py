import random
import statistics
from typing import Any, Dict

from mqtt_utils.messages.mqtt_message import MQTTMessage

from lights.actions.change_color_action import ChangeColorAction
from lights.light_controller.light_controller import LightController
from lights.settings import settings


class TurnStaticRandom(MQTTMessage):
    def __init__(self):
        super().__init__(
            settings.Mqtt.TOPIC + settings.Messages.TURN_STATIC_RANDOM)
        self.light_controller = LightController()

    def _parse_payload(self, payload):
        self._logger.debug('Executing Turn Static Random message')
        color = payload.get(settings.Messages.COLOR, None)
        if color is None:
            colors = self.light_controller.read_colors()
            color = tuple([int(statistics.mean(values))
                           for values in zip(*colors)])

        brightness = payload.get(settings.Messages.BRIGHTNESS, max(color))
        time_span = payload.get(settings.Messages.TIME_SPAN, 20)

        return color, brightness, time_span

    def execute(self, payload: Dict[str, Any]):
        self._logger.debug(f'Executing TurnStatic message with payload '
                           f'{payload}')
        color, brightness, time_span = self._parse_payload(payload)
        self.light_controller.state_on()
        self.light_controller.empty_queue()

        action = ChangeColorAction(color, brightness, time_span)
        self.light_controller.add_action(action)
