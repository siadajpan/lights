from typing import Any, Dict, Tuple, Optional

from lights.errors.incorrect_payload_exception import IncorrectPayloadException
from lights.light_controller.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnStatic(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Mqtt.TOPIC + settings.Messages.TURN_STATIC
        self.light_controller = LightController()

    def create_action(self, state: str, color: Optional[Tuple[int, int, int]]):
        self.logger.debug(f'Creating action based on state {state} and '
                          f'color {color}')
        if state == settings.Messages.OFF:
            action = LightAction(self.light_controller.turn_off,
                                 priority=settings.Actions.TURN_OFF_PRIORITY)
        elif color is None:
            action = LightAction(self.light_controller.turn_on)
        else:
            action = LightAction(self.light_controller.turn_static_color,
                                 args=[color])
        self.logger.debug(f'Action {action} created')

        return action

    def execute(self, payload: Dict[str, Any]):
        self.logger.debug(f'Executing message with payload {payload}')
        state = payload.get(settings.Messages.STATE, None)
        color = payload.get(settings.Messages.COLOR, None)

        if state is None:
            error_msg = f'Couln\'t read state from message {payload}'
            self.logger.error(error_msg)
            raise IncorrectPayloadException(error_msg)

        if color:
            self.logger.debug('Checking if color has correct format')
            color = utils.check_color_message(color)
            self.logger.debug('Color has correct format')
        else:
            self.logger.debug('Color was not specified')

        action = self.create_action(state, color)
        self.light_controller.add_action(action)
