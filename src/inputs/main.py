import json
import utime

from components import Components
from network_wrapper import NetworkWrapper


with open('config.json') as json_data:
    config = json.load(json_data)

nw = NetworkWrapper(wifi_config=config['wifi'], ubidots_config=config['ubidots'])

components = Components()

while True:

    periodic_sensors_data = components.measure_from_periodic_sensors()
    triggerred_sensors_data = {
        #'water-level': water_level
    }

    all_sensors_data = dict(periodic_sensors_data)
    all_sensors_data.update(triggerred_sensors_data)

    nw.try_sending_sensors_data(all_sensors_data)

    utime.sleep(config['behavior']['measurements_interval_sec'])