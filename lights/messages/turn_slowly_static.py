from typing import Dict, Any

from lights.actions.light_action import LightAction
from lights.errors.incorrect_payload_exception import IncorrectPayloadException
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnSlowlyStatic(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Mqtt.TOPIC + settings.Messages.TURN_SLOWLY_STATIC
        self.light_controller = LightController()

    def _calculate_steps(self, time_span):
        steps = int(time_span * 1000 / settings.Lights.SLOW_CHANGE_WAIT_MS)
        steps = max(steps, 1)
        return steps

    def _calculate_color_changes(self, color, time_span):
        color = utils.check_color_message(color)
        current_colors = self.light_controller.read_colors()
        steps = self._calculate_steps(time_span)

        leds_colors = utils.create_colors_change_table(
            current_colors, [color] * len(current_colors), steps)
        self.logger.debug(f'Changing leds of colors {current_colors} '
                          f'to {color} in {steps} steps')
        color_sets = list(zip(*leds_colors))
        return color_sets

    def calculate_brightness_changes(self, brightness, time_span):
        steps = self._calculate_steps(time_span)
        current_brightness = self.light_controller.read_brightness()
        brightness_changes = utils.create_value_change_table(
            current_brightness, brightness, steps)
        return brightness_changes

    def execute(self, payload: Dict[str, Any]):
        self.logger.debug('Executing Turn Slowly Static message')
        state = payload.get(settings.Messages.STATE, settings.Messages.ON)
        color = payload.get(settings.Messages.COLOR, None)
        if color is None:
            error_msg = f'Couln\'t read state, color or time span from ' \
                        f'message {payload}'
            self.logger.error(error_msg)
            raise IncorrectPayloadException(error_msg)

        brightness = payload.get(settings.Messages.BRIGHTNESS, max(color))
        time_span = payload.get(settings.Messages.TIME_SPAN, 10)

        self.light_controller.update_state(state)
        color_sets = self._calculate_color_changes(color, time_span)
        brightness_changes = self.calculate_brightness_changes(brightness,
                                                               time_span)

        actions = []
        for color_set, brightness in zip(color_sets, brightness_changes):
            action = LightAction(
                self.light_controller.turn_into_colors_and_wait,
                args=[color_set, brightness,
                      settings.Lights.SLOW_CHANGE_WAIT_MS / 1000]
            )
            actions.append(action)

        self.light_controller.add_actions(actions)
