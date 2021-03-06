class Mqtt:
    ADDRESS = '192.168.0.164'
    PORT = 1883
    USERNAME = 'karol'
    PASSWORD = 'klapeczki'
    TOPIC = 'lights/master_bedroom/bed/'
    ERROR_TOPIC = 'errors/lights/master_bedroom/bed/'
    STATE_TOPIC = TOPIC + 'state'


class Messages:
    TURN_OFF = 'turn_off'
    TURN_STATIC = 'turn_static'
    TURN_SLOWLY_STATIC = 'turn_slowly_static'
    TURN_STATIC_RANDOM = 'turn_static_random'
    EMPTY = 'empty'
    STATE = 'state'
    TIME_SPAN = 'time_span'
    ON = 'ON'
    OFF = 'OFF'
    BRIGHTNESS = 'brightness'
    COLOR = 'color'
    R = 'r'
    G = 'g'
    B = 'b'
    COLOR_VALUES = [R, G, B]
    STATE_VALUES = [ON, OFF]


class Lights:
    LED_AMOUNT = 12
    SLOW_CHANGE_WAIT_MS = 2000
    MIN_STEPS = 20


class Actions:
    DEFAULT_ACTION_PRIORITY = 5
    TURN_OFF_PRIORITY = 7
