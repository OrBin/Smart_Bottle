import utime
import urequests
import network


class NetworkWrapper:
    def __init__(self, wifi_ssid, wifi_password):
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password

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

