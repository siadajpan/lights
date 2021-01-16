from lights.mqtt_client.mqtt_client import MQTTClient

if __name__ == '__main__':
    client = MQTTClient()
    client.connect()
    client.loop_forever()
