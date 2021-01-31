import time

from lights.actions.light_action import LightAction


class EmptyLightAction(LightAction):
    def __init__(self):
        super().__init__(time.sleep)

    def execute(self):
        pass
