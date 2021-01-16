from lights.errors.incorrect_payload import IncorrectPayloadException


def check_color_message(message):
    try:
        assert isinstance(message, tuple)
        for el in message:
            assert isinstance(el, int)
            assert 0 <= el <= 255

    except AssertionError:
        raise IncorrectPayloadException(
            f'Color payload formatted incorrectly, '
            f'expected Tuple[uint8, uint8, uint8], '
            f'got {message}')
