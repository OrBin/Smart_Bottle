import utime
import urequests
import network
import json


class NetworkWrapper:
    def __init__(self, wifi_config, ubidots_config):
        self.wifi_ssid = wifi_config['ssid']
        self.wifi_password = wifi_config['password']
        self.ubidots_device = ubidots_config['device']
        self.ubidots_api_token = ubidots_config['api_token']

    def connect_wifi(self, timeout_sec=0):
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            sta_if.active(True)
            sta_if.connect(self.wifi_ssid, self.wifi_password)
            timeout_end = utime.time() + timeout_sec

            while not sta_if.isconnected():
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
