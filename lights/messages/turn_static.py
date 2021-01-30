from typing import Any, Dict, Tuple

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

    def create_action(self, state: str, color: Tuple[int, int, int]):
        if state:
            action = LightAction(self.light_controller.turn_static_color,
                                 args=[color])
        else:
            action = LightAction(self.light_controller.turn_off,
                                 priority=settings.Actions.TURN_OFF_PRIORITY)

        return action

    def execute(self, payload: Dict[str, Any]):
        self.logger.debug(f'Checking if payload {payload} '
                          f'is correctly formatted')
        state = payload.get(settings.Messages.STATE, None)
        color = payload.get(settings.Messages.RGB, None)

        if state is None or color is None:
            error_msg = f'Couln\'t read state or color from message {payload}'
            self.logger.error(error_msg)
            raise IncorrectPayloadException(error_msg)

        color = utils.check_color_message(color)
        self.logger.debug('Color has correct format')
        action = self.create_action(state, color)
        self.light_controller.add_action(action)
