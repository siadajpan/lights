import random
from typing import List, Optional

import numpy as np

from lights.actions.change_color_action import ChangeColorAction
from lights.actions.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.settings import settings
from lights.settings.settings import COLOR_TYPE


class GenerateRandomColorChange(LightAction):
    def __init__(self):
        super().__init__(None)
        self.light_controller = LightController()
        self.target_color: Optional[COLOR_TYPE] = None
        self.target_brightness = None
        self.time_span = settings.Lights.RANDOM_LIGHTS_TIME_SPAN
        self.color_value_changes = settings.Lights.RANDOM_LIGHTS_VALUES_CHANGES

    def evaluate_payload(self, payload) -> bool:
        self._logger.debug(f'Evaluating payload {payload} in '
                           f'GenerateRandomColorChange')
        has_state = utils.message_has_state(payload)
        has_color = utils.message_has_color(payload)

        if not has_state or not has_color:
            self._logger.debug('Payload doesn\'t have state or color')
            return False
        if self.light_controller.effect != settings.Effects.RANDOM:
            self._logger.debug('Light controller effect is not Random, it is:'
                               f'{self.light_controller.effect}')
            return False

        color = payload.get(settings.Messages.COLOR)

        self.target_color = utils.color_message_to_tuple(color)
        self.target_brightness = self.light_controller.read_max_brightness()

        return True

    def _random_colors(self) -> List[COLOR_TYPE]:
        delta = self.color_value_changes
        colors_out = []

        for pixel in range(self.light_controller.led_amount):
            color_out = []
            # r, g, b
            for i in range(3):
                change = random.randint(-delta, delta)
                color_out.append(
                    np.clip(self.target_color[i] + change, 0, 255))
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
        # When changing color during this run, make sure new color is set
        self.light_controller.empty_queue()
        colors = self._random_colors()
        brightness = self._random_brightness()
        current_action = ChangeColorAction(colors, brightness, self.time_span)
        current_action.execute()

        # Add another action like that to keep changing colors until the queue
        # is flashed by other action
        next_action = GenerateRandomColorChange()
        next_action.target_color = self.target_color
        next_action.target_brightness = self.target_brightness

        self.light_controller.add_action(next_action)
