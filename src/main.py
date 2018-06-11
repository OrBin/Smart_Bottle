import utime
from machine import Pin, PWM, SPI
from onewire import OneWire
from ds18x20 import DS18X20
from nodemcu_gpio_lcd import GpioLcd
from max7219 import Matrix8x8


ds_sensor = DS18X20(OneWire(Pin(12)))  # D6

# scan for devices on the bus
rom = ds_sensor.scan()[0]

# Convert temperature to Celsius
ds_sensor.convert_temp()

print('Temperature (Celsius, waterproof sensor):', ds_sensor.read_temp(rom))
