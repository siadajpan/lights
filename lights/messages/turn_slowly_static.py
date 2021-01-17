import time

from lights.light_controller.light_controller import LightController
from lights.messages import utils
from lights.messages.abstract_message import AbstractMessage
from lights.settings import settings


class TurnSlowlyStatic(AbstractMessage):
    def __init__(self):
        super().__init__()
        self.topic = settings.Mqtt.TOPIC + settings.Messages.TURN_SLOWLY_STATIC
        self.light_controller = LightController()

    def execute(self, *args, **kwargs):
        self.logger.debug('Executing Turn Slowly Static message')
        color, time_span = utils.check_color_value_message(args[0])
        current_colors = self.light_controller.read_colors()
        steps = int(time_span * 1000 / settings.Lights.SLOW_CHANGE_WAIT_MS)

        leds_colors = utils.create_colors_change_table(
            current_colors, [color] * len(current_colors), steps)
        self.logger.debug(f'Changing leds of colors {current_colors} '
                          f'to {color} in {steps} steps')

        for color_set in zip(*leds_colors):
            start_time = time.time()
            self.light_controller.turn_into_colors(list(color_set))
            light_turning_time = time.time() - start_time
            wait_time = settings.Lights.SLOW_CHANGE_WAIT_MS / 1000 - light_turning_time
            if wait_time > 0:
                time.sleep(wait_time)
