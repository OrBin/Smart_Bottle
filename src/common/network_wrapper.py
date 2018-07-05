import utime
import urequests
import network
import json


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
        headers = {
            'Content-Type': 'application/json',
        }

        url = 'http://things.ubidots.com/api/v1.6/devices/' + self.ubidots_device + \
              '?token=' + self.ubidots_api_token

        response = urequests.post(url, headers=headers, data=json.dumps(sensors_data))
        return response

    def try_sending_sensors_data(self, sensors_data, timeout_sec=None):
        if not self.connect_wifi(timeout_sec):
            print("No connection, Skipping")
        else:
            response = self.send_sensors_data(sensors_data)
            print(response.json())

    def _get_single_sensor_data(self, sensor_label):
        headers = {
            'Content-Type': 'application/json',
        }

        url = 'http://things.ubidots.com/api/v1.6/devices/' + self.ubidots_device + \
              '/' + sensor_label + '/lv' + \
              '?token=' + self.ubidots_api_token

        response = urequests.get(url, headers=headers)
        return response.text


    def get_variables_list(self):
        headers = {
            'Content-Type': 'application/json',
        }

        url = 'http://things.ubidots.com/api/v1.6/datasources/' + self.ubidots_device_id + \
              '/variables?token=' + self.ubidots_api_token

        response = urequests.get(url, headers=headers)
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

            return sensors_data
