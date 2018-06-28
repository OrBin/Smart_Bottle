import utime
import urequests
import network
import json


class NetworkWrapper:
    def __init__(self, wifi_config, ubidots_config):
        self.wifi_ssid = wifi_config['ssid']
        self.wifi_password = wifi_config['password']
        self.wifi_connection_timeout_sec = wifi_config['connection_timeout_sec']
        self.ubidots_device = ubidots_config['device']
        self.ubidots_api_token = ubidots_config['api_token']
        self.wifi = network.WLAN(network.STA_IF)

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
            # TODO possibly save data and send later (?)
        else:
            response = self.send_sensors_data(sensors_data)
            print(response.json())
