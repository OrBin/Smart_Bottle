from machine import Pin, ADC

from buzzer_wrapper import BuzzerWrapper
from temperature_wrapper import TemperatureWrapper
from rgb_led_wrapper import RGBLedWrapper


class Components:

    def __init__(self):
        self.buzzer = BuzzerWrapper(Pin(5))  # D1
        self.photoresistor = ADC(0)  # A0
        self.rgb_led = RGBLedWrapper(red_pin=Pin(16, Pin.OUT),  # D0
                                 green_pin=Pin(2, Pin.OUT),  # D4
                                 blue_pin=Pin(12, Pin.OUT))  # D6
        self.temperature = TemperatureWrapper(internal_sensor_pin=Pin(14),  # TODO Which pin is it?
                                              external_sensor_pin=Pin(4))  # TODO Which pin is it?

    def measure_from_periodic_sensors(self):
        light_level = self.photoresistor.read()
        temperatures = self.temperature.get_temperatures()
        return {
            'external-temperature': temperatures['external'],
            'internal-temperature': temperatures['internal'],
            'light-level': light_level
        }