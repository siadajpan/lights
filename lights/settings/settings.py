from typing import Tuple

import numpy as np


class Mqtt:
    ADDRESS = '192.168.0.164'
    PORT = 1883
    USERNAME = 'karol'
    PASSWORD = 'klapeczki'
    TOPIC = 'lights/master_bedroom/bed/'
    ERROR_TOPIC = 'errors/lights/master_bedroom/bed/'
    STATE_TOPIC = TOPIC + 'state'


class Messages:
    TURN_OFF = 'turn_off'
    TURN_STATIC = 'turn_static'
    TURN_SLOWLY_STATIC = 'turn_slowly_static'
    TURN_STATIC_RANDOM = 'turn_static_random'
    TURN_CONTINUE_RANDOM = 'turn_continue_random'
    EMPTY = 'empty'
    STATE = 'state'
    TIME_SPAN = 'time_span'
    ON = 'ON'
    OFF = 'OFF'
    BRIGHTNESS = 'brightness'
    COLOR_CHANGE_VALUES = 'color_change_values'
    COLOR = 'color'
    EFFECT = 'effect'
    R = 'r'
    G = 'g'
    B = 'b'
    COLOR_VALUES = [R, G, B]
    STATE_VALUES = [ON, OFF]


class Effects:
    STANDARD = 'Standard'
    RANDOM = 'Random'


def get_effects():
    effects = [v for k, v in Effects.__dict__.items()
               if not k.startswith('__')]

    return effects


class Lights:
    LED_AMOUNT = 12
    SLOW_CHANGE_WAIT_MS = 2000
    MIN_STEPS = 20
    RANDOM_LIGHTS_TIME_SPAN = 2
    RANDOM_LIGHTS_VALUES_CHANGES = 50


class Actions:
    DEFAULT_ACTION_PRIORITY = 5
    TURN_OFF_PRIORITY = 7


COLOR_TYPE = Tuple[np.uint8, np.uint8, np.uint8]
if __name__ == '__main__':
    print(get_effects())