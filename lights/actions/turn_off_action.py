from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class TurnOff(LightAction):
    def __init__(self):
        self.light_controller = LightController()
        super().__init__(method=self.light_controller.turn_off)

    def evaluate_payload(self, payload) -> bool:
        """
        Check if payload is type {'state': 'OFF'}
        :raises: IncorrectPayloadException if state has wrong value
        """
        self._logger.debug(f'Evaluating payload {payload} in TurnOff')
        has_state = utils.message_has_state(payload)

        if not has_state:
            return False

        state_off = payload[settings.Messages.STATE] == settings.Messages.OFF

        return state_off
