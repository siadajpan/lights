from lights.light_controller.light_action import LightAction
from lights.light_controller.light_controller import LightController
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnOff(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Mqtt.TOPIC + settings.Messages.TURN_OFF
        self.light_controller = LightController()

    def execute(self, *args, **kwargs):
        self.logger.debug('Executing Turn Off message')

        action = LightAction(self.light_controller.turn_off,
                             priority=settings.Actions.TURN_OFF_PRIORITY)
        self.light_controller.add_action(action)
