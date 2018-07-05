import math
import mpu6050
from machine import I2C, Pin


class GyroscopeWrapper:

    def __init__(self, scl_pin, sda_pin):
        i2c = I2C(scl=scl_pin, sda=sda_pin)
        self.accelerometer = mpu6050.accel(i2c)
        self._check_gyro_values()

    def _measure_gyro_values_norm(self):
        gyro_values = self.accelerometer.get_values()
        gx, gy, gz = gyro_values['GyX'], gyro_values['GyY'], gyro_values['GyZ']
        self.last_gyro_values_norm = math.sqrt(gx*gx + gy*gy + gz*gz)

    def is_