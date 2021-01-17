import logging
import queue
import time
from typing import Tuple, List

import board
import neopixel
from singleton_decorator import singleton

from lights.light_controller.light_action import LightAction
from lights.settings import settings


@singleton
class LightController:
    def __init__(self):
        self._led_amount = settings.Lights.LED_AMOUNT
        self._pixels = neopixel.NeoPixel(board.D18, self._led_amount)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._actions_queue = queue.Queue()
        self._stop = False
        self.executing_priority = 0

    def turn_off(self):
        self._logger.info('Turning off lights')
        for i in range(self._led_amount):
            self._pixels[i] = (0, 0, 0)

    def turn_static_color(self, color: Tuple[int, int, int]):
        for i in range(self._led_amount):
            self._pixels[i] = color

    def turn_into_colors(self, colors: List[Tuple[int, int, int]]):
        for i, color in enumerate(colors):
            self._pixels[i] = color

    def read_colors(self) -> List[Tuple[int, int, int]]:
        return eval(str(self._pixels))

    def add_action(self, action):
        self.add_actions([action])

    def add_actions(self, actions: List[LightAction]):
        if actions[0].priority <= self.executing_priority:
            self._actions_queue.put(actions)
        else:
            self.empty_queue()
            self._actions_queue.put(actions)

    def run(self):
        while not self._stop:
            if self._actions_queue.empty():
                self.executing_priority = 0

            light_action: LightAction = self._actions_queue.get()
            self.executing_priority = light_action.priority
            light_action.execute()

    def empty_queue(self):
        while not self._actions_queue.empty():
            self._actions_queue.get()

    def stop(self):
        self._stop = True
        self._actions_queue.put(LightAction(time.sleep, 0))
