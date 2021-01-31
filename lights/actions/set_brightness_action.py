from typing import Dict, Any

from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class SetBrightness(LightAction):
    def __init__(self):
        self.light_controller = LightController()
        super().__init__(method=self.light_controller.set_brightness)

    def evaluate_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Check if payload is type {'state': 'ON', 'brightness': int}
        :raises: IncorrectPayloadException if state or brightness have wrong
        value
        """
        has_state = utils.message_has_state(payload)
        has_brightness = utils.message_has_brightness(payload)
        keys = payload.keys()

        if not has_state or not has_brightness or len(keys) > 2:
            return False

        if payload[settings.Messages.STATE] == settings.Messages.ON:
            self.arguments = [payload.get(settings.Messages.BRIGHTNESS)]
            return True

        return False
