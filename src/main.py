import json
from machine import Pin, ADC

from buzzer_wrapper import BuzzerWrapper
from temperature_wrapper import TemperatureWrapper
from network_wrapper import NetworkWrapper
from notes import *






photoresistor = ADC(0)  #A0
light_level = photoresistor.read()
print('Light level (0 to 1024):', light_level)


red = Pin(16, Pin.OUT)  # D0
green = Pin(2, Pin.OUT)  # D4
blue = Pin(12, Pin.OUT)  # D6
red.off()
blue.on()
green.off()

tw = TemperatureWrapper(internal_sensor_pin=Pin(14), external_sensor_pin=Pin(4))
internal_temperature = tw.get_internal_temperature()
print('Temperature (Celsius, waterproof internal sensor):', internal_temperature)
external_temperature = tw.get_external_temperature()
print('Temperature (Celsius, external sensor):', external_temperature)

bw = BuzzerWrapper(Pin(5))  # D1
bw.play_drinking_notification()

with open('config.json') as json_data:
    config = json.load(json_data)



nw = NetworkWrapper(wifi_config=config['wifi'], ubidots_config=config['ubidots'])

if not nw.connect_wifi(config['wifi']['connection_timeout_sec']):
    print("No connection, Skipping")
    # TODO save data and send later (?)
else:
    response = nw.send_sensors_data({
        'external-temperature': external_temperature,
        'internal-temperature': internal_temperature,
        'light-level': light_level,
        #'water-level': water_level
    })
    print(response.json())
