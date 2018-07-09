from json import load as json_load
from utime import sleep

from components import Components
from network_wrapper import NetworkWrapper


with open('config.json') as json_data:
    config = json_load(json_data)

nw = NetworkWrapper(wifi_config=config['wifi'], ubidots_config=config['ubidots'])

components = Components(config)

bottle_capacity = config['bottle']['bottle_capacity_ml']

while True:
    sensors_data = components.measure_from_periodic_sensors()
    sensors_data['bottle-capacity'] = bottle_capacity

    nw.try_sending_sensors_data(sensors_data)

    sleep(config['behavior']['measurements_interval_sec'])
