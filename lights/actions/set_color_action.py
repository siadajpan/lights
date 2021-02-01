from typing import Dict, Any, Tuple, Optional

from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class SetColor(LightAction):
    def __init__(self):
        self.light_controller = LightController()
        super().__init__(method=self.light_controller.turn_static_color)
        self._color: Optional[Tuple[int, int, int]] = None
        self._brightness: Optional[int] = None

    def set_color(self, color: Tuple[int, int, int]):
        self._color = color

    def set_brightness(self, brightness: int):
        self._brightness = brightness

    def evaluate_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Check if payload is type
        {
            'state': 'ON',
            'color': {'r': int, 'g': int, 'b': int}
        }
        :raises: IncorrectPayloadException if state, brightness or color have
        wrong value
        """
        has_state = utils.message_has_state(payload)
        has_color = utils.message_has_color(payload)

        if not has_state or not has_color:
            return False
        if sum([has_state, has_color]) != 2:
            return False
        if payload[settings.Messages.STATE] == settings.Messages.OFF:
            return False

        self._logger.debug('Received payload that fits to set color action')
        color = payload.get(settings.Messages.COLOR)

        self.set_color(utils.color_message_to_tuple(color))
        self.set_brightness(self.light_controller.get_brightness())

        self._logger.debug(f'Received color: {self._color} and brightness: '
                           f'{self._brightness}')
        return True

    def execute(self):
        self.light_controller.update_state(settings.Messages.ON)
        if not self._color or not self._brightness:
            raise ValueError('Color or brightness not set')

        self.arguments = [self._color, self._brightness]
        super().execute()
