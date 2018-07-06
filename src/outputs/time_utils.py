def unix_time():
    from utime import time
    SECONDS_IN_30_YEARS = 946684800
    return time() + SECONDS_IN_30_YEARS

def check_drinking_notification_required(last_drinking_timestamp_sec, last_notification_timestamp_sec, required_drinking_frequency_sec):
    now_timestamp_sec = unix_time()

    if now_timestamp_sec - last_drinking_timestamp_sec < required_drinking_frequency_sec:
        return False

    if now_timestamp_sec - last_notification_timestamp_sec < required_drinking_frequency_sec:
        return False

    return True

def sync_ntp(network_wrapper):
    from utime import sleep
    from ntptime import settime

    while not network_wrapper.connect_wifi():
        print("No connection, retrying")
        sleep(1)

    while True:
        try:
            settime()
            break
        except:
            sleep(1)

