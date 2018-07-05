import utime
from onewire import OneWire
from ds18x20 import DS18X20
from dht import DHT11


class TemperatureWrapper:
    def __init__(self, internal_sensor_pin, external_sensor_pin):
        self.internal_sensor = DS18X20(OneWire(internal_sensor_pin))

        # scan for devices on the bus
        self.rom = self.internal_sensor.scan()[0]

        self.external_sensor = DHT11(external_sensor_pin)

    def get_internal_temperature(self):
        # convert_temp() must be executed to initiate a temperature reading,
        # then wait at least 750ms before reading the value.

        self.internal_sensor.convert_temp()
        utime.sleep_ms(750)
        return self.internal_sensor.read_temp(self.rom)

    def get_external_temperature(self):
        self.external_sensor.measure()
        return self.external_sensor.temperature()

    def get_temperatures(self):
        return {
            'internal': self.get_internal_temperature(),
            'external': self.get_external_temperature()
        }
