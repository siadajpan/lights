import random
from typing import Tuple

import numpy as np

from lights.actions.change_color_action import ChangeColorAction


class GenerateRandomColorChange(ChangeColorAction):
    def __init__(self, color: Tuple[np.uint8, np.uint8, np.uint8],
                 brightness, time_span, color_value_changes: int = 10):
        self.color: Tuple[np.uint8, np.uint8, np.uint8] = color
        self.brightness = brightness
        self.time_span = time_span
        self.color_value_changes = color_value_changes
        new_color = self._random_color()

        super().__init__(new_color, brightness, time_span)

    def _random_color(self) -> Tuple[np.uint8, np.uint8, np.uint8]:
        color = list(self.color)
        delta = self.color_value_changes
        # r, g, b
        for i in range(3):
            change = random.randint(-delta, delta)
            color[i] = np.clip(color[i] + change, 0, 255)

        return tuple(np.asarray(color, dtype=np.uint8))

    def execute(self):
        super().execute()
        # Add another action like that to keep changing colors until the queue
        # is flashed by other action
        next_action = GenerateRandomColorChange(
            self.color, self.brightness, self.time_span,
            self.color_value_changes
        )
        self.light_controller.add_action(next_action)
