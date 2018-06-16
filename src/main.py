import json
import utime
import urequests
import network
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
internal_temperature = wp_temp_sensor.read_temp(rom)
print('Temperature (Celsius, waterproof internal sensor):', internal_temperature)

photoresistor = ADC(0)  #A0
light_level = photoresistor.read()
print('Light level (0 to 1024):', light_level)


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
    external_temperature = dht_sensor.temperature()
    print('Temperature (Celsius, external sensor):', external_temperature)
except OSError as os_error:
    if os_error.args[0] == 110: # ETIMEDOUT
        print("Cannot access sensor: timed out")
    else:
        print(os_error)



with open('config.json') as json_data:
    config = json.load(json_data)

def connect(timeout_sec=0):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(config['wifi']['ssid'], config['wifi']['password'])
        timeout_end = utime.time() + timeout_sec

        while not sta_if.isconnected():
            if utime.time() > timeout_end:
                return False

        return True


headers = {
    'Content-Type': 'application/json',
}

data = json.dumps({
    'external-temperature': external_temperature,
    'internal-temperature': internal_temperature,
    'light-level': light_level,
    #'water-level': water_level
})

url = 'http://things.ubidots.com/api/v1.6/devices/' + config['ubidots']['device'] + '?token=' + config['ubidots']['api_token']

if not connect(config['wifi']['connection_timeout_sec']):
    print("No connection, Skipping")
    # TODO save data and send later (?)
else:
    response = urequests.post(url, headers=headers,  data=data)
    print(response.json())
