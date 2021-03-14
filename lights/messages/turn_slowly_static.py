from typing import Dict, Any

from mqtt_utils.messages.mqtt_message import MQTTMessage

from lights.actions.change_color_action import ChangeColorAction
from lights.errors.incorrect_payload_exception import IncorrectPayloadException
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class TurnSlowlyStatic(MQTTMessage):
    def __init__(self):
        super().__init__(settings.Mqtt.TOPIC + settings.Messages.TURN_SLOWLY_STATIC)
        self.light_controller = LightController()

    def _parse_payload(self, payload):
        self._logger.debug('Executing Turn Slowly Static message')
        color = payload.get(settings.Messages.COLOR, None)
        if color is None:
            error_msg = f'Couln\'t read state, color or time span from ' \
                        f'message {payload}'
            self._logger.error(error_msg)
            raise IncorrectPayloadException(error_msg)

        color = utils.color_message_to_tuple(color)
        brightness = payload.get(settings.Messages.BRIGHTNESS, max(color))
        time_span = payload.get(settings.Messages.TIME_SPAN, 10)

        return color, brightness, time_span

    def execute(self, payload: Dict[str, Any]):
        color, brightness, time_span = self._parse_payload(payload)
        self.light_controller.state_on()
        self.light_controller.empty_queue()
        action = ChangeColorAction(color, brightness, time_span)

        self.light_controller.add_action(action)
