from typing import Dict, Any, Tuple, Optional

from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class SetEffect(LightAction):
    def __init__(self):
        self.light_controller = LightController()
        super().__init__(method=self.light_controller.set_effect)
        self._effect = None

    def evaluate_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Check if payload is type
        {
            'state': 'ON',
            'effect': str
        }
        :raises: IncorrectPayloadException if state, brightness or color have
        wrong value
        """
        self._logger.debug(f'Evaluating payload {payload} in SetEffect')
        has_state = utils.message_has_state(payload)
        has_effect = utils.message_has_effect(payload)

        if not has_state or not has_effect:
            return False
        if payload[settings.Messages.STATE] == settings.Messages.OFF:
            return False

        self._logger.debug('Received payload that fits to set color action')
        self._effect = payload.get(settings.Messages.EFFECT)

        self._logger.debug(f'Received effect: {self._effect}')

        return True

    def execute(self):
        if self._effect is None:
            raise ValueError('Effect not set. Run evaluate_payload before '
                             'calling execute')

        # After setting effect, front-end send the same message with empty
        # effect. Do nothing
        if self._effect == '':
            return

        self.arguments = [self._effect]
        super().execute()
