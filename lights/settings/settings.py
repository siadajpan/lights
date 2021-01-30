class Mqtt:
    ADDRESS = '192.168.0.164'
    PORT = 1883
    USERNAME = 'karol'
    PASSWORD = 'klapeczki'
    TOPIC = 'lights/master_bedroom/bed/'
    ERROR_TOPIC = 'errors/lights/master_bedroom/bed/'


class Messages:
    COLOR = 'color'
    TURN_OFF = 'turn_off'
    TURN_STATIC = 'turn_static'
    TURN_SLOWLY_STATIC = 'turn_slowly_static'
    EMPTY = 'empty'


class Lights:
    LED_AMOUNT = 12
    SLOW_CHANGE_WAIT_MS = 50


class Actions:
    DEFAULT_ACTION_PRIORITY = 5
    TURN_OFF_PRIORITY = 7
