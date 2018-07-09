HEADERS = {
    'Content-Type': 'application/json',
}


class NetworkWrapper:

    def __init__(self, wifi_config, ubidots_config):
        from network import WLAN, STA_IF
        self.wifi_ssid = wifi_config['ssid']
        self.wifi_password = wifi_config['password']
        self.wifi_connection_timeout_sec = wifi_config['connection_timeout_sec']
        self.ubidots_api_token = ubidots_config['api_token']
        self.ubidots_device = ubidots_config['device']
        self.ubidots_device_id = ubidots_config['device_id']
        self.wifi = WLAN(STA_IF)
        self.variables = None

    def connect_wifi(self, timeout_sec=None):
        from utime import time
        if timeout_sec is None:
            timeout_sec = self.wifi_connection_timeout_sec

        if self.wifi.isconnected():
            return True

        self.wifi.active(True)
        self.wifi.connect(self.wifi_ssid, self.wifi_password)
        timeout_end = time() + timeout_sec

        while not self.wifi.isconnected():
            if time() > timeout_end:
                return False

        return True

    def send_sensors_data(self, sensors_data):
        from urequests import post
        from json import dumps as json_dumps
        url = 'http://things.ubidots.com/api/v1.6/devices/' + self.ubidots_device + \
              '?token=' + self.ubidots_api_token

        response = post(url, headers=HEADERS, data=json_dumps(sensors_data))
        return response

    def try_sending_sensors_data(self, sensors_data, timeout_sec=None):
        if not self.connect_wifi(timeout_sec):
            print("No connection, Skipping")
            return False
        else:
            response = self.send_sensors_data(sensors_data)
            return True


    def _get_measured_variables_data(self):
        from urequests import get
        response = get(url='http://things.ubidots.com/api/v1.6/datasources/' + self.ubidots_device_id + \
                                 '/variables?token=' + self.ubidots_api_token + '&tag=measured',
                                 headers=HEADERS)
        return response.json()['results']

    def get_sensors_data(self, timeout_sec=None):

        if not self.connect_wifi(timeout_sec):
            print("No connection, Skipping")
        else:

            results = self._get_measured_variables_data()

            sensors_data = { variable['label']: variable['last_value']['value'] for variable in results }

            water_level_results = [variable for variable in results if variable['label'] == 'water-level'][0]
            sensors_data['last-drinking-timestamp'] = water_level_results['last_value']['timestamp']

            return sensors_data
