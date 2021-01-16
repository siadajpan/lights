class Mqtt:
    ADDRESS = '192.168.0.201'
    PORT = '1883'
    USERNAME = 'karol'
    PASSWORD = 'klapeczki'
    TOPIC = 'lights/master_bedroom/bed'
    ERROR_TOPIC = 'errors/lights'


class Messages:
    COLOR = 'color'
    TURN_OFF = 'turn_off'
    TURN_STATIC = 'turn_static'

class Lights:
    LED_AMOUNT = 7