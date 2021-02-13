import logging
from datetime import datetime

from mqtt_utils.message_manager import MessageManager

from lights.light_controller.light_controller import LightController
from lights.messages.turn_slowly_static import TurnSlowlyStatic
from lights.messages.turn_static import TurnStatic
from lights.messages.turn_static_random import TurnStaticRandom
from lights.settings import settings

if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")

    logging.basicConfig(
        filename=f'/home/pi/projects/lights/logs/{dt_string}.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG)

    logging.info('Starting lights controller')
    light_controller = LightController()
    light_controller.start()

    MESSAGES = [TurnStatic(), TurnSlowlyStatic(), TurnStaticRandom()]
    logging.info('Starting message manager')
    message_manager = MessageManager(MESSAGES, settings.Mqtt.ERROR_TOPIC)
    message_manager.connect(settings.Mqtt.ADDRESS, settings.Mqtt.PORT)
    light_controller.update_publish_method(message_manager.publish)
    message_manager.start()

    try:
        message_manager.run()
    except KeyboardInterrupt:
        light_controller.stop()
        message_manager.stop()
