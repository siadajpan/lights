import logging
import queue
import statistics
import time
from threading import Thread
from typing import Tuple, List, Callable, Optional

import board
import neopixel
from singleton_decorator import singleton

from lights.light_controller.empty_light_action import EmptyLightAction
from lights.light_controller.light_action import LightAction
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
        self._default_lights_value: List[Tuple[int, int, int]] = \
            [(1, 1, 1), ] * self._led_amount

    def update_publish_method(self, publish_method):
        """
        Update method that is used for signalling state change
        """
        self._publish_method = publish_method

    def turn_off(self):
        self._default_lights_value = self.read_colors()
        self._logger.info(f'Turning off lights, saving lights state: '
                          f'{self._default_lights_value}')
        self.turn_static_color(color=(0, 0, 0))

    def turn_on(self):
        self._default_lights_value = self.read_colors()
        self._logger.info(f'Turning on lights to color: {self._default_lights_value}')
        self.turn_into_colors(self._default_lights_value)

    def turn_static_color(self, color: Tuple[int, int, int]):
        for i in range(self._led_amount):
            self._pixels[i] = color

        message = ColorStateMessage(color)
        self._logger.debug(f'Publishing state message {message}')
        self._publish_method(message.topic, message.payload)

    def turn_into_colors(self, colors: List[Tuple[int, int, int]]):
        for i, color in enumerate(colors):
            self._pixels[i] = color

        mean_color = tuple([int(statistics.mean(values))
                            for values in zip(*colors)])
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
