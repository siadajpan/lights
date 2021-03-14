import random
from typing import Any, Dict

from mqtt_utils.messages.mqtt_message import MQTTMessage

from lights.actions.generate_random_color_change import \
    GenerateRandomColorChange
from lights.light_controller.light_controller import LightController
from lights.settings import settings


class TurnContinueRandom(MQTTMessage):
    """
    Message from MQTT client to switch light continuously around target color,
    by maximum of some delta
    """
    def __init__(self):
        super().__init__(
            settings.Mqtt.TOPIC + settings.Messages.TURN_CONTINUE_RANDOM)
        self.light_controller = LightController()

    def _parse_payload(self, payload):
        self._logger.debug('Executing Turn Static Random message')
        color = payload.get(settings.Messages.COLOR, None)
        if color is None:
            color = tuple([random.randint(0, 255) for _ in range(3)])

        brightness = payload.get(settings.Messages.BRIGHTNESS, max(color))
        time_span = payload.get(settings.Messages.TIME_SPAN, 20)
        delta = payload.get(settings.Messages.COLOR_CHANGE_VALUES, 20)

        return color, brightness, time_span, delta

    def execute(self, payload: Dict[str, Any]):
        self._logger.debug(f'Executing TurnContinueRandom message with payload '
                           f'{payload}')
        color, brightness, time_span, delta = self._parse_payload(payload)
        self.light_controller.state_on()
        self.light_controller.empty_queue()

        action = GenerateRandomColorChange(color, brightness, time_span, delta)

        self.light_controller.add_action(action)