import logging
import math
from typing import Tuple, Any, List

from lights.errors.developer_exception import DeveloperException
from lights.errors.incorrect_payload_exception import IncorrectPayloadException

logger = logging.getLogger('lights_utils')


def evaluate_message(message) -> Any:
    try:
        message = eval(message)
        return message
    except SyntaxError:
        error_message = f'Message payload formatted incorrectly, ' \
                        f'got {message}'
        raise IncorrectPayloadException(error_message)


def check_color_message(message) -> Tuple[int, int, int]:
    try:
        message = evaluate_message(message)
        assert isinstance(message, tuple)
        for el in message:
            assert isinstance(el, int)
            assert 0 <= el <= 255

        return message
    except AssertionError:
        error_message = f'Color payload formatted incorrectly, ' \
                        f'expected (uint8, uint8, uint8), ' \
                        f'got {message}'
        logger.error(error_message)
        raise IncorrectPayloadException(error_message)
    except Exception as ex:
        error_message = f'Checking color payload raised exception ' \
                        f'expected (uint8, uint8, uint8), ' \
                        f'got {message}, exception: {ex}'
        logger.error(error_message)
        raise IncorrectPayloadException(error_message)


def check_color_value_message(message) -> Tuple[Tuple[int, int, int], float]:
    try:
        message = evaluate_message(message)
        assert len(message) == 2
        color = check_color_message(str(message[0]))
        value = message[1]
        assert (isinstance(value, float) or isinstance(value, int))
        assert (value > 0)
        return color, float(value)

    except AssertionError:
        error_message = f'Color-value payload formatted incorrectly, ' \
                        f'expected (uint8, uint8, uint8), float ' \
                        f'got {message}'
        logger.error(error_message)
        raise IncorrectPayloadException(error_message)
    except Exception as ex:
        error_message = f'Checking payload evaluation raised exception ' \
                        f'got {message}, exception: {ex}'
        logger.error(error_message)
        raise IncorrectPayloadException(error_message)


def create_color_change_table(from_color, to_color, steps) \
        -> List[Tuple[int, int, int]]:
    # list 0-1 of multipliers length of steps
    change_table = [- 0.5 * math.cos(x / (steps - 1) * math.pi) + 0.5 for x in
                    range(steps)]

    values_out = []
    for from_value, to_value in zip(from_color, to_color):
        value_change = to_value - from_value
        values_out.append(
            [int(x * value_change + from_value) for x in change_table])

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
        raise DeveloperException(error_message)

    colors_list_out = []
    for from_color, to_color in zip(from_colors, to_colors):
        colors_list_out.append(
            create_color_change_table(from_color, to_color, steps))

    return colors_list_out
