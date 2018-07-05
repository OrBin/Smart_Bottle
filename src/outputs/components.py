from machine import Pin, ADC

from buzzer_wrapper import BuzzerWrapper
from rgb_led_wrapper import RGBLedWrapper


class Components:

    def __init__(self):
        self.buzzer = BuzzerWrapper(Pin(15))  # D8
        self.rgb_led = RGBLedWrapper(red_pin=Pin(16, Pin.OUT),  # D0
                                 green_pin=Pin(2, Pin.OUT),  # D4
                                 blue_pin=Pin(12, Pin.OUT))  # D6