import random
from typing import Tuple, List

import numpy as np

from lights.actions.change_color_action import ChangeColorAction
from lights.light_controller.light_controller import LightController
from lights.settings import settings
from lights.settings.settings import COLOR_TYPE


class GenerateRandomColorChange(ChangeColorAction):
    def __init__(self, color: COLOR_TYPE, brightness: np.uint8,
                 time_span, color_value_changes: int = 10):
        self.light_controller = LightController()
        self.target_color: COLOR_TYPE = color
        self.target_brightness = brightness
        self.time_span = time_span
        self.color_value_changes = color_value_changes
        new_colors = self._random_colors()
        new_brightness = self._random_brightness()

        super().__init__(new_colors, new_brightness, time_span)

    def evaluate_payload(self, payload) -> bool:
        if not super().evaluate_payload(payload):
            return False

        if self.light_controller.effect != settings.Effects.RANDOM:
            return False

        return True

    def _random_colors(self) -> List[COLOR_TYPE]:
        delta = self.color_value_changes
        colors_out = []
        for pixel in range(self.light_controller.led_amount):
            color_out = []
            # r, g, b
            for i in range(3):
                change = random.randint(-delta, delta)
                color_out.append(np.clip(self.target_color[i] + change, 0, 255))
            colors_out.append(tuple(np.asarray(color_out, dtype=np.uint8)))

        return colors_out

    def _random_brightness(self) -> List[np.uint8]:
        delta = self.color_value_changes
        brightness_out = []
        for pixel in range(self.light_controller.led_amount):
            brightness = self.target_brightness + random.randint(-delta, delta)
            brightness = np.clip(brightness, 0, 255)
            brightness_out.append(brightness)

        return brightness_out

    def execute(self):
        super().execute()
        # Add another action like that to keep changing colors until the queue
        # is flashed by other action
        next_action = GenerateRandomColorChange(
            self.target_color, self.target_brightness, self.time_span,
            self.color_value_changes
        )
        self.light_controller.add_action(next_action)
