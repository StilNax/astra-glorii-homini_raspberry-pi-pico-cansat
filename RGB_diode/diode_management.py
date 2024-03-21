from machine import Pin


class RGB_led:
    def __init__(self):
        # RGB diode pin initialization
        self.red_diode = Pin(15, Pin.OUT)
        self.green_diode = Pin(14, Pin.OUT)
        self.blue_diode = Pin(18, Pin.OUT)

    def red(self):
        self.blue_diode.value(0)
        self.green_diode.value(0)
        self.red_diode.value(1)

    def green(self):
        self.blue_diode.value(0)
        self.green_diode.value(1)
        self.red_diode.value(0)

    def blue(self):
        self.blue_diode.value(1)
        self.green_diode.value(0)
        self.red_diode.value(0)

    def cyan(self):
        self.blue_diode.value(1)
        self.green_diode.value(1)
        self.red_diode.value(0)

    def purple(self):
        self.blue_diode.value(1)
        self.green_diode.value(0)
        self.red_diode.value(1)

    def yellow(self):
        self.blue_diode.value(0)
        self.green_diode.value(1)
        self.red_diode.value(1)

    def white(self):
        self.blue_diode.value(1)
        self.green_diode.value(1)
        self.red_diode.value(1)

    def off(self):
        self.blue_diode.value(0)
        self.green_diode.value(0)
        self.red_diode.value(0)
