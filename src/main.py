import utime
from machine import Pin, PWM, SPI
import max7219
from nodemcu_gpio_lcd import GpioLcd


lcd = None
led_matrix = None
buzzer = None
led = None


def initialize_components():

    lcd = GpioLcd(rs_pin=Pin(16),
                  enable_pin=Pin(5),
                  d4_pin=Pin(4),
                  d5_pin=Pin(0),
                  d6_pin=Pin(2),
                  d7_pin=Pin(12),
                  num_lines=2, num_columns=20)

    spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
    led_matrix = max7219.Matrix8x8(spi, Pin(15), 1)
    led_matrix.brightness(0)  # 0-15
    led_matrix.fill(0)

