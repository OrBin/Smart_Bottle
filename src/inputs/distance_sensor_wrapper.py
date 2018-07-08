import math
from hcsr04 import HCSR04


class DistanceSensorWrapper:

    MEASUREMENTS_COUNT = 250

    def __init__(self, trigger_pin, echo_pin, bottle_height_cm, ml_per_cm):
        self.sensor = HCSR04(trigger_pin=trigger_pin,
                             echo_pin=echo_pin)
        self.bottle_height_cm = bottle_height_cm
        self.ml_per_cm = ml_per_cm

    def get_water_level(self):
        distances = []
        for _ in range(self.MEASUREMENTS_COUNT):
            distances.append(self.sensor.distance_cm())

        distances = sorted(distances)
        distances = distances[len(distances) * 7 // 8:]

        squared_distances = [d*d for d in distances]
        rms = math.sqrt(sum(squared_distances) / len(squared_distances))

        final_distance_cm = rms
        water_height_cm = self.bottle_height_cm - final_distance_cm

        water_level_ml = water_height_cm * self.ml_per_cm

        if water_level_ml < self.ml_per_cm / 2:
            return 0

        return water_level_ml
