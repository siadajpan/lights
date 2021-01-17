from typing import Tuple

from lights.errors.incorrect_payload import IncorrectPayloadException


def check_color_message(message) -> Tuple[int, int, int]:
    error_message = f'Color payload formatted incorrectly, ' \
                    f'expected Tuple[uint8, uint8, uint8], ' \
                    f'got {message}'
    try:
        message = eval(message)
        assert isinstance(message, tuple)
        for el in message:
            assert isinstance(el, int)
            assert 0 <= el <= 255

        return message

    except AssertionError:
        raise IncorrectPayloadException(error_message)
    except SyntaxError:
        raise IncorrectPayloadException(error_message)
