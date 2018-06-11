import utime
from machine import Pin, PWM, SPI, ADC
from onewire import OneWire
from ds18x20 import DS18X20
from nodemcu_gpio_lcd import GpioLcd
from max7219 import Matrix8x8


wp_temp_sensor = DS18X20(OneWire(Pin(12)))  # D6

# scan for devices on the bus
rom = wp_temp_sensor.scan()[0]

# Convert temperature to Celsius
wp_temp_sensor.convert_temp()

print('Temperature (Celsius, waterproof sensor):', wp_temp_sensor.read_temp(rom))

photoresistor = ADC(0)  #A0
print('Photoresistor value (0 to 1024):', photoresistor.read())
