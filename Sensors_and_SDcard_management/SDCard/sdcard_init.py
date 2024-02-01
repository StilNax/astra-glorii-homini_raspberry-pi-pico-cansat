from machine import Pin, SPI
from SDCard.sdcard import SDCard
import uos


def sdcard_init():
    # Defining sd card pinout
    sd_card_cs = Pin(13, Pin.OUT)
    sd_card_spi = SPI(1,
                      baudrate=1000000,
                      polarity=0,
                      phase=0,
                      bits=8,
                      firstbit=SPI.MSB,
                      sck=Pin(10),
                      mosi=Pin(11),
                      miso=Pin(12))
    sd = SDCard(sd_card_spi, sd_card_cs)
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
