from typing import Any, Dict

from mqtt_utils.messages.mqtt_message import MQTTMessage

from lights.actions.set_brightness_action import SetBrightness
from lights.actions.set_color_action import SetColor
from lights.actions.turn_off_action import TurnOff
from lights.actions.turn_on_action import TurnOn
from lights.errors.incorrect_payload_exception import IncorrectPayloadException
from lights.light_controller.light_controller import LightController
from lights.settings import settings

ACTIONS = [TurnOff(), TurnOn(), SetBrightness(), SetColor()]


class TurnStatic(MQTTMessage):
    def __init__(self):
        super().__init__(settings.Mqtt.TOPIC + settings.Messages.TURN_STATIC)
        self.light_controller = LightController()

    def create_action(self, payload):
        for action in ACTIONS:
            if action.evaluate_payload(payload):
                return action

        return None

    def execute(self, payload: Dict[str, Any]):
        self._logger.debug(f'Executing TurnStatic message with payload '
                           f'{payload}')
        action = self.create_action(payload)
        if not action:
            msg = f'Turn static message has unexpected payload: {payload}'
            raise IncorrectPayloadException(msg)

        self.light_controller.add_action(action)
