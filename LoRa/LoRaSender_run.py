from machine import Pin, SPI
from LoRa.sx127x import SX127x


class LoRa_run:
    def __init__(self):
        # LoRa configuration
        lora_default = {
            'frequency': 433e6,
            'frequency_offset': 0,
            'tx_power_level': 20,
            'signal_bandwidth': 125e3,
            'spreading_factor': 8,
            'coding_rate': 5,
            'preamble_length': 8,
            'implicitHeader': False,
            'sync_word': 0x22,
            'enable_CRC': True,
            'invert_IQ': False,
            'debug': False,
        }

        lora_pins = {
            'dio_0': 22,
            'ss': 1,
            'reset': 27,
            'sck': 2,
            'miso': 0,
            'mosi': 3,
        }

        lora_spi = SPI(
                       0,
                       baudrate=10000000, polarity=0, phase=0,
                       bits=8, firstbit=SPI.MSB,
                       sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
                       mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
                       miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP),
                      )

        self.lora = SX127x(lora_spi, pins=lora_pins, parameters=lora_default)

    def send(self, data):
        # print("LoRa Sender")
        # print('TX: {}'.format(data))

        self.lora.println(data)
