import logging
from datetime import datetime

from lights.light_controller.light_controller import LightController
from lights.messages.message_manager import MessageManager
from lights.mqtt_client.mqtt_client import MQTTClient

if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")

    logging.basicConfig(filename=f'/home/pi/projects/lights/logs/{dt_string}.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.info('Starting lights controller')
    light_controller = LightController()
    light_controller.start()

    logging.info('Starting mqtt client')
    client = MQTTClient()
    client.connect()

    logging.info('Starting message manager')
    message_manager = MessageManager(client.message_queue, client.publish)
    light_controller.update_publish_method(message_manager.publish)
    message_manager.start()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        light_controller.stop()
        message_manager.stop()
