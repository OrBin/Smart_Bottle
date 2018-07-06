import json
from utime import sleep

import time_utils
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

time_utils.sync_ntp(nw)
components = Components()
components.rgb_led.set_colors(False, False, False)

last_notification_timestamp_sec = 0

while True:
    sensors_data = nw.get_sensors_data()

    r, g, b = calculate_temperature_color(float(sensors_data['internal-temperature']),
                                          float(sensors_data['external-temperature']))
    components.rgb_led.set_colors(r, g, b)

    components.seven_segment.number(int(sensors_data['water-level']))

    if time_utils.check_drinking_notification_required(sensors_data['last-drinking-timestamp'] // 1000,
                                            last_notification_timestamp_sec,
                                            config['behavior']['required_drinking_frequency_minutes'] * 60):
        components.buzzer.play_drinking_notification()
        last_notification_timestamp_sec = time_utils.unix_time()

    sleep(config['behavior']['measurements_interval_sec'])

