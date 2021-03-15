from typing import Tuple, Dict, Any

from mqtt_utils.messages.mqtt_message import MQTTMessage

from lights.messages import utils
from lights.settings import settings
import json

from lights.settings.settings import COLOR_TYPE


class EffectStateMessage(MQTTMessage):
    """
    Message that is used for status update. Color and brightness status
    are sent on each light switch
    """
    def __init__(self, effect: settings.Effects):
        super().__init__(settings.Mqtt.STATE_TOPIC)
        self.payload = self._generate_payload(effect)

    def _generate_payload(self, effect):
        payload = {
            settings.Messages.EFFECT: effect,
        }
        self._logger.debug(f'Generating payload to send, {payload}')

        return json.dumps(payload)

    def execute(self, payload: Dict[str, Any]):
        raise NotImplementedError('Effect state message doesn\'t have execute '
                                  'method')
