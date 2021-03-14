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
        if payload[settings.Messages.STATE] == settings.Messages.OFF:
            return False
        if self.light_controller.effect != settings.Effects.STANDARD:
            return False

        self._logger.debug('Received payload that fits to set color action')
        color = payload.get(settings.Messages.COLOR)

        self._color = utils.color_message_to_tuple(color)
        self._brightness = self.light_controller.read_max_brightness()
        self._logger.debug(f'Received color: {self._color} and brightness: '
                           f'{self._brightness}')
        return True

    def execute(self):
        self.light_controller.state_on()
        if not self._color:
            raise ValueError('Color not set. Run evaluate_payload before '
                             'calling execute')
        if not self._brightness:
            self._brightness = max(self._color)

        self.arguments = [self._color, self._brightness]
        super().execute()
