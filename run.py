import logging
from datetime import datetime

from lights.mqtt_client.mqtt_client import MQTTClient

if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")

    logging.basicConfig(filename=f'/ħome/pi/projects/lights/logs/{dt_string}.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logging.info('Starting lights')
    client = MQTTClient()
    client.connect()
    client.loop_forever()
