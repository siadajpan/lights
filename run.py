import logging

from lights.mqtt_client.mqtt_client import MQTTClient

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    client = MQTTClient()
    client.connect()
    client.loop_forever()
