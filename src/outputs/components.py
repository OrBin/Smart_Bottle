from machine import Pin, ADC
from tm1637 import TM1637

from buzzer_wrapper import BuzzerWrapper
from rgb_led_wrapper import RGBLedWrapper


class Components:

    def __init__(self):
        self.buzzer = BuzzerWrapper(Pin(15, Pin.OUT))  # D8
        self.rgb_led = RGBLedWrapper(red_pin=Pin(16, Pin.OUT),  # D0
                                 green_pin=Pin(2, Pin.OUT),  # D4
                                 blue_pin=Pin(12, Pin.OUT))  # D6
        self.seven_segment = TM1637(clk=Pin(5, Pin.OUT),  # D1
                                    dio=Pin(4, Pin.OUT))  # D2
        self.led = Pin(14, Pin.OUT)  # D5