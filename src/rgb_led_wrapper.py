class RGBLedWrapper:

    def __init__(self, red_pin, green_pin, blue_pin):
        self.red = red_pin
        self.green = green_pin
        self.blue = blue_pin

    def set_colors(self, red: bool, green: bool, blue: bool):
        self.red.value(red)
        self.green.value(green)
        self.blue.value(blue)

