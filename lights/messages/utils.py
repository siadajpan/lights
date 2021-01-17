from typing import Tuple

from lights.errors.incorrect_payload import IncorrectPayloadException


def evaluate_message(message) -> bool:
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
                        f'expected Tuple[uint8, uint8, uint8], ' \
                        f'got {message}'
        raise IncorrectPayloadException(error_message)
