import utime
from machine import PWM
from notes import E4


class BuzzerWrapper:
    def __init__(self, pin):
        # set up pin PWM timer for output to buzzer or speaker
        self.buzzer = PWM(pin, freq=400)
        self.buzzer.duty(50)

    def play_drinking_notification(self):
        tune = [E4, 0] * 3

        for i in tune:
            if i == 0:
                self.buzzer.duty(0)  # 0% = 0/100 * 1024 = 0
            else:
                self.buzzer.freq(i)  # change frequency for change tone
                self.buzzer.duty(307)  # 30% = 30/100 * 1024 = 307

            utime.sleep_ms(50)

