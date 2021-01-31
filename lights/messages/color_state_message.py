from typing import Tuple, Dict, Any

from lights.messages import utils
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings
import json


class ColorStateMessage(AbstractMessage):
    """
    Message that is used for status update. Color and brightness status
    are sent on each light switch
    """
    def __init__(self, color: Tuple[int, int, int], brightness, state: str):
        super().__init__()
        self.topic = settings.Mqtt.STATE_TOPIC
        self.payload = self._generate_payload(color, brightness, state)

    def _generate_payload(self, color: Tuple[int, int, int], brightness: int,
                          state: str):
        """
        Create payload that has state, color and brightness
        """
        payload = {
            settings.Messages.STATE: state,
            settings.Messages.BRIGHTNESS: brightness,
            settings.Messages.COLOR: utils.color_to_dict(color)
        }
        self.logger.debug(f'Generating payload to send, {payload}')

        return json.dumps(payload)

    def execute(self, payload: Dict[str, Any]):
        raise NotImplementedError('Color state message doesn\'t have execute '
                                  'method')
