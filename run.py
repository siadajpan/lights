import logging

from lights.mqtt_client.mqtt_client import MQTTClient

if __name__ == '__main__':
    logging.root.setLevel(logging.DEBUG)
    logging.info('Starting lights')
    client = MQTTClient()
    client.connect()
    client.loop_forever()
