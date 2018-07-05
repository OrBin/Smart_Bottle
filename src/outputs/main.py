import json
import utime

from components import Components
from network_wrapper import NetworkWrapper


with open('config.json') as json_data:
    config = json.load(json_data)

nw = NetworkWrapper(wifi_config=config['wifi'], ubidots_config=config['ubidots'])

components = Components()
components.rgb_led.set_colors(False, False, True)
components.buzzer.play_drinking_notification()



while True:

    sensors_data = nw.get_sensors_data()
    print(sensors_data)
    utime.sleep(config['behavior']['measurements_interval_sec'])
