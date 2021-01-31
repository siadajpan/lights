from typing import Dict, Any

from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class SetColor(LightAction):
    def __init__(self):
        self.light_controller = LightController()
        super().__init__(method=self.light_controller.turn_static_color)

    def evaluate_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Check if payload is type
        {
            'state': 'ON',
            'brightness': int, [optional]
            'color': {'r': int, 'g': int, 'b': int}
        }
        :raises: IncorrectPayloadException if state, brightness or color have
        wrong value
        """
        has_state = utils.message_has_state(payload)
        has_brightness = utils.message_has_brightness(payload)
        has_color = utils.message_has_color(payload)
        keys = payload.keys()

        if not has_state or not has_color:
            return False
        if sum([has_state, has_color, has_brightness]) != len(keys):
            return False

        if payload[settings.Messages.STATE] == settings.Messages.ON:
            color = payload.get(settings.Messages.COLOR)
            self.arguments = utils.color_message_to_tuple(color)
            self._logger.debug(f'Updating set color arguments to '
                               f'{self.arguments}')
            return True

        return False
