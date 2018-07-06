import json
import utime

from components import Components
from network_wrapper import NetworkWrapper


def calculate_temperature_color(internal_temperature, external_temperature):

    temperature_range = config['behavior']['temperature_range']
    external_temperature_allowed_offset = config['behavior']['external_temperature_allowed_offset']

    if internal_temperature > temperature_range['max']:
        return (True, False, False)  # Hot - Red light
    elif internal_temperature < temperature_range['min']:
        return (False, False, True)  # Cold - Blue light
    else:
        if external_temperature - external_temperature_allowed_offset > temperature_range['max']:
            return (True, False, False)  # Hot - Red light
        elif external_temperature + external_temperature_allowed_offset < temperature_range['min']:
            return (False, False, True)  # Cold - Blue light
        else:
            return (False, True, False)  # Good - Green light

with open('config.json') as json_data:
    config = json.load(json_data)

nw = NetworkWrapper(wifi_config=config['wifi'], ubidots_config=config['ubidots'])



components = Components()
components.rgb_led.set_colors(False, False, False)
components.buzzer.play_drinking_notification()

while True:
    sensors_data = nw.get_sensors_data()
    #print(sensors_data)

    r, g, b = calculate_temperature_color(float(sensors_data['internal-temperature']),
                                          float(sensors_data['external-temperature']))
    components.rgb_led.set_colors(r, g, b)

    print(sensors_data['water-level'])

    utime.sleep(config['behavior']['measurements_interval_sec'])

