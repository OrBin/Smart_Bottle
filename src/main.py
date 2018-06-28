import json
from machine import Pin, ADC

from buzzer_wrapper import BuzzerWrapper
from temperature_wrapper import TemperatureWrapper
from network_wrapper import NetworkWrapper
from rgb_led_wrapper import RGBLedWrapper


with open('config.json') as json_data:
    config = json.load(json_data)

photoresistor = ADC(0)  #A0
light_level = photoresistor.read()
print('Light level (0 to 1024):', light_level)

rlw = RGBLedWrapper(red_pin=Pin(16, Pin.OUT),  # D0
                    green_pin=Pin(2, Pin.OUT),  # D4
                    blue_pin=Pin(12, Pin.OUT))  # D6
rlw.set_colors(False, False, True)

tw = TemperatureWrapper(internal_sensor_pin=Pin(14), external_sensor_pin=Pin(4))
temperatures = tw.get_temperatures()
print('Temperature (Celsius, waterproof internal sensor):', temperatures['internal'])
print('Temperature (Celsius, external sensor):', temperatures['external'])

bw = BuzzerWrapper(Pin(5))  # D1
bw.play_drinking_notification()

nw = NetworkWrapper(wifi_config=config['wifi'], ubidots_config=config['ubidots'])
if not nw.connect_wifi(config['wifi']['connection_timeout_sec']):
    print("No connection, Skipping")
    # TODO save data and send later (?)
else:
    response = nw.send_sensors_data({
        'external-temperature': temperatures['external'],
        'internal-temperature': temperatures['internal'],
        'light-level': light_level,
        #'water-level': water_level
    })
    print(response.json())
