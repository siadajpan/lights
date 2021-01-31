import logging
import queue
import statistics
import time
from threading import Thread
from typing import Tuple, List, Callable, Optional

import board
import neopixel
from singleton_decorator import singleton

from lights.actions.empty_light_action import EmptyLightAction
from lights.actions.light_action import LightAction
from lights.messages import utils
from lights.messages.color_state_message import ColorStateMessage
from lights.settings import settings


@singleton
class LightController(Thread):
    def __init__(self):
        super().__init__()
        self._led_amount = settings.Lights.LED_AMOUNT
        self._pixels = neopixel.NeoPixel(board.D18, self._led_amount)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._actions_queue = queue.Queue()
        self._stop_thread = False
        self.executing_priority = 0
        self._publish_method: Optional[Callable[[str, str], None]] = None
        self._colors: List[Tuple[int, int, int]] = \
            [(2, 2, 2), ] * self._led_amount
        self._brightness = 1

    def update_publish_method(self, publish_method):
        """
        Update method that is used for signalling state change
        """
        self._publish_method = publish_method

    def turn_off(self):
        self._colors = self.read_colors()
        self._logger.info(f'Turning off lights, saving lights state: '
                          f'{self._colors}')
        self.turn_static_color(color=(0, 0, 0))

    def turn_on(self):
        self._logger.info(
            f'Turning on lights to color: {self._colors}')
        self.turn_into_colors(self._colors)

    def turn_static_color(self, color: Tuple[int, int, int]):
        self._logger.debug(f'Turning into static color: {color}')
        self.turn_into_colors([color, ] * self._led_amount)

    def read_brightness(self):
        max_value = max([max(values) for values in self._colors])
        return max_value

    def set_brightness(self, brightness: int):
        """
        Update colors of pixels to change brightness
        """
        self._logger.debug(f'Settings brightness {brightness}')
        curr_brightness = self.read_brightness()
        if curr_brightness == 0:
            self._colors = [(2, 2, 2), ] * self._led_amount
            curr_brightness = 2

        scale = brightness / curr_brightness
        self._logger.debug(f'Scaling colors by {scale}')
        new_colors = [tuple([int(scale * value) for value in color])
                      for color in self._colors]

        self.turn_into_colors(new_colors)

    def turn_into_colors(self, colors: List[Tuple[int, int, int]]):
        self._logger.debug(f'Turning into colors: {colors}')
        for i, color in enumerate(colors):
            self._pixels[i] = color

        self._colors = self._pixels
        self._brightness = self.read_brightness()

        mean_color = tuple([int(statistics.mean(values))
                            for values in zip(*self._colors)])
        assert len(mean_color) == 3
        message = ColorStateMessage(mean_color)
        self._publish_method(message.topic, message.payload)

    def turn_into_colors_and_wait(self, colors, time_span):
        start_time = time.time()
        self.turn_into_colors(colors)
        light_turning_time = time.time() - start_time
        wait_time = time_span - light_turning_time
        if wait_time > 0:
            time.sleep(wait_time)

    def read_colors(self) -> List[Tuple[int, int, int]]:
        return eval(str(self._pixels))

    def add_action(self, action: LightAction):
        self._logger.debug(f'Adding {action} to queue')
        self.add_actions([action])

    def add_actions(self, actions: List[LightAction]):
        self._logger.debug(f'Adding {len(actions)} actions to queue')
        # If new action has higher priority, empty queue
        if actions[0].priority > self.executing_priority:
            self.empty_queue()

        # Put new actions to the queue
        for action in actions:
            self._actions_queue.put(action)

    def run(self):
        while not self._stop_thread:
            if self._actions_queue.empty():
                self._logger.debug('Light controller waiting for actions')
                # Reset current priority -> All action can take place now
                self.executing_priority = 0

            light_action: LightAction = self._actions_queue.get()

            # Update current priority to current action
            self.executing_priority = light_action.priority
            light_action.execute()
        self._logger.debug('Exiting')

    def empty_queue(self):
        while not self._actions_queue.empty():
            self._actions_queue.get()

    def stop(self):
        self._logger.debug('Stopping')
        self._stop_thread = True
        self._actions_queue.put(EmptyLightAction())
