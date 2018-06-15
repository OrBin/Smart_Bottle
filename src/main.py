import utime
from machine import Pin, PWM, SPI, ADC
from onewire import OneWire
from ds18x20 import DS18X20
from dht import DHT11
#from nodemcu_gpio_lcd import GpioLcd
#from max7219 import Matrix8x8

from notes import *


wp_temp_sensor = DS18X20(OneWire(Pin(14)))  # D5

# scan for devices on the bus
rom = wp_temp_sensor.scan()[0]

# Convert temperature to Celsius
wp_temp_sensor.convert_temp()

print('Temperature (Celsius, waterproof internal sensor):', wp_temp_sensor.read_temp(rom))

photoresistor = ADC(0)  #A0
print('Photoresistor value (0 to 1024):', photoresistor.read())


red = Pin(16, Pin.OUT)
green = Pin(2, Pin.OUT)
blue = Pin(13, Pin.OUT)
red.off()
blue.on()
green.off()


# set up pin PWM timer for output to buzzer or speaker
buzzer = PWM(Pin(12), freq=400)  # D6
buzzer.duty(50)

tune = [E4, 0] * 3

for i in tune:
    if i == 0:
        buzzer.duty(0)  # 0% = 0/100 * 1024 = 0
    else:
        buzzer.freq(i)  # change frequency for change tone
        buzzer.duty(307)  # 30% = 30/100 * 1024 = 307

    utime.sleep_ms(50)


dht_sensor = DHT11(Pin(4))

try:
    dht_sensor.measure()
    print('Temperature (Celsius, external sensor):', dht_sensor.temperature())
except OSError as os_error:
    if os_error.args[0] == 110: # ETIMEDOUT
        print("Cannot access sensor: timed out")
    else:
        print(os_error)
