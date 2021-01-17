import logging
from typing import Tuple, List

import board
import neopixel
from singleton_decorator import singleton

from lights.settings import settings


@singleton
class LightController:
    def __init__(self):
        self.led_amount = settings.Lights.LED_AMOUNT
        self.pixels = neopixel.NeoPixel(board.D18, self.led_amount)
        self.logger = logging.getLogger(self.__class__.__name__)

    def turn_off(self):
        self.logger.info('Turning off lights')
        for i in range(self.led_amount):
            self.pixels[i] = (0, 0, 0)

    def turn_static_color(self, color: Tuple[int, int, int]):
        self.logger.info(f'Turning lights to {color}')
        for i in range(self.led_amount):
            self.pixels[i] = color

    def turn_into_colors(self, colors: List[Tuple[int, int, int]]):
        self.logger.info(f'Turning ligths to {colors}')
        for i, color in enumerate(colors):
            self.pixels[i] = color

    def read_colors(self) -> List[Tuple[int, int, int]]:
        self.logger.info(f'Reading colors')

        return eval(str(self.pixels))
