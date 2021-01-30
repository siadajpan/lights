from typing import Tuple

from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class ColorStateMessage(AbstractMessage):
    """
    Message that is used for status update. Color and brightness status
    are sent on each light switch
    """
    def __init__(self, color: Tuple[int, int, int]):
        super().__init__()
        self.topic = settings.Mqtt.STATE_TOPIC
        self.payload = self._generate_payload(color)

    def _generate_payload(self, color):
        """
        Create payload that has state, color and brightness
        """
        brightness = max(color)
        state = 'on' if brightness else 'off'
        payload = {
            settings.Messages.STATE: state,
            settings.Messages.BRIGHTNESS: brightness,
            settings.Messages.COLOR: color,
        }

        return payload

    def execute(self, *args, **kwargs):
        raise NotImplementedError('Color state message doesn\'t have execute '
                                  'method')
