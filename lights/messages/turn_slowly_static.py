from typing import Dict, Any

from lights.errors.incorrect_payload_exception import IncorrectPayloadException
from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnSlowlyStatic(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Mqtt.TOPIC + settings.Messages.TURN_SLOWLY_STATIC
        self.light_controller = LightController()

    def execute(self, payload: Dict[str, Any]):
        self.logger.debug('Executing Turn Slowly Static message')
        state = payload.get(settings.Messages.STATE, None)
        color = payload.get(settings.Messages.COLOR, None)
        brightness = payload.get(settings.Messages.BRIGHTNESS, None)
        time_span = payload.get(settings.Messages.TIME_SPAN, None)

        if state is None or color is None:
            error_msg = f'Couln\'t read state, color or time span from ' \
                        f'message {payload}'
            self.logger.error(error_msg)
            raise IncorrectPayloadException(error_msg)

        color = utils.check_color_message(color)
        current_colors = self.light_controller.read_colors()
        steps = int(time_span * 1000 / settings.Lights.SLOW_CHANGE_WAIT_MS)
        steps = max(steps, 1)

        leds_colors = utils.create_colors_change_table(
            current_colors, [color] * len(current_colors), steps)
        self.logger.debug(f'Changing leds of colors {current_colors} '
                          f'to {color} in {steps} steps')
        color_sets = list(zip(*leds_colors))

        current_brightness = self.light_controller.read_brightness()
        brightness_changes = utils.create_value_change_table(
            current_brightness, brightness, steps)

        actions = []
        for color_set, brightness in zip(color_sets, brightness_changes):
            action = LightAction(
                self.light_controller.turn_into_colors_and_wait,
                args=[color_set, brightness,
                      settings.Lights.SLOW_CHANGE_WAIT_MS / 1000]
            )
            actions.append(action)

        self.light_controller.add_actions(actions)
