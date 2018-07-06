import utime
import urequests
import network
import json


HEADERS = {
    'Content-Type': 'application/json',
}


class NetworkWrapper:

    def __init__(self, wifi_config, ubidots_config):
        self.wifi_ssid = wifi_config['ssid']
        self.wifi_password = wifi_config['password']
        self.wifi_connection_timeout_sec = wifi_config['connection_timeout_sec']
        self.ubidots_api_token = ubidots_config['api_token']
        self.ubidots_device = ubidots_config['device']
        self.ubidots_device_id = ubidots_config['device_id']
        self.wifi = network.WLAN(network.STA_IF)
        self.variables = None

    def connect_wifi(self, timeout_sec=None):
        if timeout_sec is None:
            timeout_sec = self.wifi_connection_timeout_sec

        if self.wifi.isconnected():
            return True

        self.wifi.active(True)
        self.wifi.connect(self.wifi_ssid, self.wifi_password)
        timeout_end = utime.time() + timeout_sec

        while not self.wifi.isconnected():
            if utime.time() > timeout_end:
                return False

        return True

    def send_sensors_data(self, sensors_data):
        url = 'http://things.ubidots.com/api/v1.6/devices/' + self.ubidots_device + \
              '?token=' + self.ubidots_api_token

        response = urequests.post(url, headers=HEADERS, data=json.dumps(sensors_data))
        return response

    def try_sending_sensors_data(self, sensors_data, timeout_sec=None):
        if not self.connect_wifi(timeout_sec):
            print("No connection, Skipping")
            return False
        else:
            response = self.send_sensors_data(sensors_data)
            print(response.json())
            return True

    def _get_single_sensor_data(self, sensor_label):
        url = 'http://things.ubidots.com/api/v1.6/devices/' + self.ubidots_device + \
              '/' + sensor_label + '/lv' + \
              '?token=' + self.ubidots_api_token

        response = urequests.get(url, headers=HEADERS)
        return response.text


    def get_variables_list(self):
        url = 'http://things.ubidots.com/api/v1.6/datasources/' + self.ubidots_device_id + \
              '/variables?token=' + self.ubidots_api_token

        response = urequests.get(url, headers=HEADERS)
        results = response.json()

        return [variable['label'] for variable in results['results']]

    def get_sensors_data(self, timeout_sec=None):

        if not self.connect_wifi(timeout_sec):
            print("No connection, Skipping")
        else:

            if not self.variables:
                self.variables = self.get_variables_list()

            sensors_data = {}

            for variable_label in self.variables:
                sensors_data[variable_label] = self._get_single_sensor_data(variable_label)

            url = 'http://things.ubidots.com/api/v1.6/devices/' + self.ubidots_device + \
                  '/water-level/values' + \
                  '?token=' + self.ubidots_api_token

            water_level_response = urequests.get(url, headers=HEADERS)
            water_level_results = water_level_response.json()
            sensors_data['last-drinking-timestamp'] = water_level_results['results'][0]['timestamp']

            return sensors_data
