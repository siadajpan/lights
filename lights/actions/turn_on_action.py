from typing import Dict, Any

from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class TurnOn(LightAction):
    def __init__(self):
        self.light_controller = LightController()
        super().__init__(method=self.light_controller.turn_on)

    def evaluate_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Check if payload is type {'state': 'ON'}
        :raises: IncorrectPayloadException if state has wrong value
        """
        self._logger.debug(f'Evaluating payload {payload} in TurnOn')
        has_state = utils.message_has_state(payload)
        keys = payload.keys()

        if not has_state or len(keys) > 1:
            self._logger.debug('Payload doesn\t have state or has more in the'
                               'payload than just setting state')
            return False

        state_on = payload[settings.Messages.STATE] == settings.Messages.ON

        return state_on
