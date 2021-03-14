from typing import Tuple, Dict, Any, List

import numpy as np

from lights.actions.change_color_action import ChangeColorAction
from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings


class ChangeColorsAction(ChangeColorAction):
    def __init__(self, colors: List[Tuple[np.uint8, np.uint8, np.uint8]],
                 brightness: List[np.uint8], time_span: int):
        self.light_controller = LightController()
        super().__init__(colors[0], brightness[0], time_span)
        self.colors: List[Tuple[np.uint8, np.uint8, np.uint8]] = colors
        self.brightness = brightness
        self.time_span = time_span

    def _calculate_color_changes(self, colors, time_span):
        current_colors = self.light_controller.read_colors()
        if len(colors) != len(current_colors):
            raise RuntimeError('Trying to calculate color changes but lengths '
                               'of colors and leds don\'t match')
        steps = self._calculate_steps(time_span)

        leds_colors = utils.create_colors_change_table(
            current_colors, colors, steps)
        self._logger.debug(f'Changing leds of colors {current_colors} '
                           f'to {colors} in {steps} steps')
        color_sets = list(zip(*leds_colors))
        return color_sets
