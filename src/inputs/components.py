from machine import Pin, ADC

from temperature_wrapper import TemperatureWrapper
from distance_sensor_wrapper import DistanceSensorWrapper

class Components:

    def __init__(self, config):
        self.photoresistor = ADC(0)  # A0
        self.temperature = TemperatureWrapper(internal_sensor_pin=Pin(14),  # D5
                                              external_sensor_pin=Pin(4))  # D2
        self.ml_per_cm = config['bottle']['ml_per_cm']
        self.bottle_capacity_ml = config['bottle']['bottle_capacity_ml']
        self.distance = DistanceSensorWrapper(trigger_pin=16,  # D0
                                              echo_pin=0,  # D3
                                              bottle_height_cm=config['bottle']['bottle_height_cm'],
                                              ml_per_cm=self.ml_per_cm)
        self.prev_water_level = None

    def measure_from_periodic_sensors(self):
        light_level = self.photoresistor.read()
        temperatures = self.temperature.get_temperatures()

        measurements = {
            'external-temperature': temperatures['external'],
            'internal-temperature': temperatures['internal'],
            'light-level': light_level
        }

        water_level = self.distance.get_water_level()

        if (self.prev_water_level is None) or \
                (abs(self.prev_water_level - water_level) > self.ml_per_cm) or \
                (water_level > self.bottle_capacity_ml):
            measurements['water-level'] = water_level

        self.prev_water_level = water_level

        return measurements
