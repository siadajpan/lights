import json
import logging
import math
from typing import Tuple, Any, List, Dict, Optional

import numpy as np

from lights.errors.developer_exception import DeveloperException
from lights.errors.incorrect_payload_exception import IncorrectPayloadException
from lights.settings import settings

logger = logging.getLogger('lights_utils')


def payload_from_json(message: Optional[str]) -> Optional[Dict[str, Any]]:
    if not message:
        return None

    try:
        logger.debug(f'Loading message into dict {message}')
        message_dict = json.loads(message)
        logger.debug(f'Message loaded {message_dict}')
        return message_dict
    except Exception as ex:
        error_message = f'Received a message that is not json: {message}, {ex}'
        logger.error(error_message)
        raise IncorrectPayloadException(error_message)


def color_to_dict(color: Tuple[int, int, int]):
    dict_color = {}
    for desc, value in zip(settings.Messages.COLOR_VALUES, color):
        dict_color[desc] = value
    return dict_color


def message_has_state(message: Dict[str, Any]) -> bool:
    state = message.get(settings.Messages.STATE, None)
    if not state:
        return False

    if state not in settings.Messages.STATE_VALUES:
        msg = f'Expected state within {settings.Messages.STATE_VALUES}, ' \
              f'got: {state}'
        logger.error(msg)
        raise IncorrectPayloadException(msg)

    return True


def message_has_color(message: Dict[str, Any]) -> bool:
    color = message.get(settings.Messages.COLOR, None)
    if not color:
        return False

    if not check_color_message(color):
        msg = f'Expected state within {settings.Messages.STATE_VALUES}, ' \
              f'got: {color}'
        logger.error(msg)
        raise IncorrectPayloadException(msg)

    return True


def message_has_effect(message: Dict[str, Any]) -> bool:
    effect = message.get(settings.Messages.EFFECT, None)
    if not effect:
        return False

    if not check_color_message(effect):
        msg = f'Expected state within {settings.Messages.STATE_VALUES}, ' \
              f'got: {effect}'
        logger.error(msg)
        raise IncorrectPayloadException(msg)

    return True


def message_has_brightness(message: Dict[str, Any]) -> bool:
    brightness = message.get(settings.Messages.BRIGHTNESS, None)
    if not brightness:
        return False

    try:
        assert isinstance(brightness, int)
        assert 0 <= brightness
    except AssertionError:
        msg = f'Expected brightness as int greater or equal 0, ' \
              f'got: {brightness}'
        logger.error(msg)
        raise IncorrectPayloadException(msg)

    return True


def color_message_to_tuple(message: Dict[str, Any]) \
        -> Tuple[np.uint8, np.uint8, np.uint8]:
    r = message.get(settings.Messages.R, None)
    g = message.get(settings.Messages.G, None)
    b = message.get(settings.Messages.B, None)
    message_tuple = (r, g, b)

    return message_tuple


def check_color_message(message: Dict[str, Any]) \
        -> Tuple[np.uint8, np.uint8, np.uint8]:
    message_tuple = color_message_to_tuple(message)
    try:
        for el in message_tuple:
            assert isinstance(el, int)
            assert 0 <= el <= 255

        return message_tuple
    except AssertionError:
        error_message = f'Color payload formatted incorrectly, ' \
                        'expected {\'r\': uint8, \'g\': uint8, \'b\': ' \
                        f'uint8), got {message}'
        logger.error(error_message)
        raise IncorrectPayloadException(error_message)
    except Exception as ex:
        error_message = f'Checking color payload raised exception ' \
                        'expected {\'r\': uint8, \'g\': uint8, \'b\': ' \
                        f'uint8), got {message}, exception: {ex}'
        logger.error(error_message)
        raise IncorrectPayloadException(error_message)


def create_sine_value_change_table(from_value, to_value, steps):
    # list 0-1 of multipliers length of steps
    change_table = [- 0.5 * math.cos(x / (steps - 1) * math.pi) + 0.5 for x in
                    range(steps)]
    value_change = to_value - from_value
    change_table = [int(x * value_change + from_value) for x in change_table]

    return change_table


def create_linear_value_change_table(from_value, to_value, steps):
    change_table = np.linspace(from_value, to_value, steps)

    return change_table


def create_color_change_table(from_color, to_color, steps) \
        -> List[Tuple[int, int, int]]:
    values_out = []
    for from_value, to_value in zip(from_color, to_color):
        change_table = create_linear_value_change_table(
            from_value, to_value, steps)
        values_out.append(change_table)

    colors_out = [(r, g, b) for r, g, b in zip(*values_out)]

    return colors_out


def create_colors_change_table(from_colors, to_colors, steps) \
        -> List[List[Tuple[int, int, int]]]:
    """
    Create list of colors that each of LED needs to go through to
    switch from one color to another
    :param from_colors: list of LED starting colors
    :param to_colors: list of LED ending colors
    :param steps: steps for switch from one color set to another
    :return: list of color changes for each led
    """
    if len(from_colors) != len(to_colors):
        error_message = f'Creating table of color change. Length of ' \
                        f'from_colors and to_colors are not equal'
        logger.error(error_message)
        raise DeveloperException(error_message)

    colors_list_out = []
    for from_color, to_color in zip(from_colors, to_colors):
        colors_list_out.append(
            create_color_change_table(from_color, to_color, steps))

    return colors_list_out
