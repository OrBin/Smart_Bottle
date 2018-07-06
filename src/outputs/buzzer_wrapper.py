from utime import sleep_ms
from machine import PWM


class BuzzerWrapper:
    def __init__(self, pin):
        # set up pin PWM timer for output to buzzer or speaker
        self.buzzer = PWM(pin, freq=400)
        self.buzzer.duty(0)

    def play_drinking_notification(self):
        tune = [330, 0] * 3  # E4 is 330 hz

        for i in tune:
            if i == 0:
                self.buzzer.duty(0)  # 0% = 0/100 * 1024 = 0
            else:
                self.buzzer.freq(i)  # change frequency for change tone
                self.buzzer.duty(307)  # 30% = 30/100 * 1024 = 307

            sleep_ms(50)

