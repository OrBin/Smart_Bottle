from machine import Pin, ADC

from temperature_wrapper import TemperatureWrapper


class Components:

    def __init__(self):
        self.photoresistor = ADC(0)  # A0
        self.temperature = TemperatureWrapper(internal_sensor_pin=Pin(14),  # D5
                                              external_sensor_pin=Pin(4))  # D2

    def measure_from_periodic_sensors(self):
        light_level = self.photoresistor.read()
        temperatures = self.temperature.get_temperatures()
        return {
            'external-temperature': temperatures['external'],
            'internal-temperature': temperatures['internal'],
            'light-level': light_level
        }