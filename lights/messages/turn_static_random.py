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
            color = tuple([random.randint(0, 255) for _ in range(3)])

        brightness = payload.get(settings.Messages.BRIGHTNESS, max(color))
        time_span = payload.get(settings.Messages.TIME_SPAN, 20)

        return color, brightness, time_span

    def execute(self, payload: Dict[str, Any]):
        self._logger.debug(f'Executing TurnStatic message with payload '
                           f'{payload}')
        color, brightness, time_span = self._parse_payload(payload)
        self.light_controller.empty_queue()
        self.light_controller.state_on()
        self.light_controller.set_effect(settings.Effects.STANDARD)
        leds = self.light_controller.led_amount
        action = ChangeColorAction([color, ] * leds, [brightness, ] * leds,
                                   time_span)

        self.light_controller.add_action(action)
