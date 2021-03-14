from typing import Tuple, Dict, Any

import numpy as np

from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class ChangeColorAction(LightAction):
    def __init__(self, color: Tuple[np.uint8, np.uint8, np.uint8],
                 brightness: np.uint8, time_span: int):
        self.light_controller = LightController()
        super().__init__(method=None)
        self.colors: Tuple[np.uint8, np.uint8, np.uint8] = color
        self.brightness = brightness
        self.time_span = time_span

    def _calculate_steps(self, time_span):
        steps = int(time_span * 1000 / settings.Lights.SLOW_CHANGE_WAIT_MS)
        steps = max(steps, settings.Lights.MIN_STEPS)
        return steps

    def _calculate_color_changes(self, color, time_span):
        current_colors = self.light_controller.read_colors()
        steps = self._calculate_steps(time_span)

        leds_colors = utils.create_colors_change_table(
            current_colors, [color] * len(current_colors), steps)
        self._logger.debug(f'Changing leds of colors {current_colors} '
                           f'to {color} in {steps} steps')
        color_sets = list(zip(*leds_colors))
        return color_sets

    def calculate_brightness_changes(self, brightness, time_span):
        steps = self._calculate_steps(time_span)
        current_brightness = self.light_controller.read_max_brightness()
        brightness_changes = utils.create_linear_value_change_table(
            current_brightness, brightness, steps)

        return brightness_changes

    def evaluate_payload(self, payload) -> bool:
        """
        Check if payload is at least type {'state': 'ON'}
        :raises: IncorrectPayloadException if state has wrong value
        """
        has_state = utils.message_has_state(payload)

        if not has_state:
            return False

        state_off = payload[settings.Messages.STATE] == settings.Messages.OFF

        return state_off

    def execute(self):
        """
        Add multiple light color actions into light_controller
        """
        color_sets = self._calculate_color_changes(self.colors, self.time_span)
        brightness_changes = self.calculate_brightness_changes(
            self.brightness, self.time_span)
        wait_time = self.time_span / len(color_sets)

        for color_set, brightness in zip(color_sets, brightness_changes):
            action = LightAction(
                self.light_controller.turn_into_colors_and_wait,
                args=[color_set, brightness, wait_time]
            )
            self.light_controller.add_action(action)
