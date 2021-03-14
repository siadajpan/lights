import random
from typing import Tuple, List

import numpy as np

from lights.actions.change_colors_action import ChangeColorsAction


class GenerateRandomColorChange(ChangeColorsAction):
    def __init__(self, color: Tuple[np.uint8, np.uint8, np.uint8],
                 brightness, time_span, color_value_changes: int = 10):
        self.color: Tuple[np.uint8, np.uint8, np.uint8] = color
        self.brightness = brightness
        self.time_span = time_span
        self.color_value_changes = color_value_changes
        new_colors = self._random_colors()

        super().__init__(new_colors, brightness, time_span)

    def _random_colors(self) -> List[Tuple[np.uint8, np.uint8, np.uint8]]:
        color = list(self.color)
        delta = self.color_value_changes
        color_number = len(self.light_controller.read_colors())
        colors_out = []
        for pixel in range(color_number):
            color_out = []
            # r, g, b
            for i in range(3):
                change = random.randint(-delta, delta)
                color_out[i] = np.clip(color[i] + change, 0, 255)
            colors_out.append(tuple(np.asarray(color_out, dtype=np.uint8)))

        return colors_out

    def execute(self):
        super().execute()
        # Add another action like that to keep changing colors until the queue
        # is flashed by other action
        next_action = GenerateRandomColorChange(
            self.color, self.brightness, self.time_span,
            self.color_value_changes
        )
        self.light_controller.add_action(next_action)
