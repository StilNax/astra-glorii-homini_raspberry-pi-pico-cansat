from Sensors.BMP.bmp280 import *
from Sensors.BMP.bmp_calculation_methods import altitude_HYP, altitude_IBF
from machine import I2C, Pin


class BMP_run:
    def __init__(self):
        # Defining BMP pinout and calibration

        # Caliberation error in pressure
        self.ERROR = -3  # hPa

        I2C_id = 1        # positional argument - I2C id
        sclPin = Pin(27)  # named argument - serial clock pin
        sdaPin = Pin(26)  # named argument - serial data pin
        freq = 1000000    # named argument - i2c frequency

        # Initiate I2C
        bmp_i2c_object = I2C(I2C_id, scl=sclPin, sda=sdaPin, freq=freq)

        # create a BMP 280 object
        self.bmp280_object = BMP280(bmp_i2c_object,
                                    addr=0x76,  # change it
                                    use_case=BMP280_CASE_WEATHER)

        # configure the sensor
        self.bmp280_object.power_mode = BMP280_POWER_NORMAL
        self.bmp280_object.oversample = BMP280_OS_HIGH
        self.bmp280_object.temp_os = BMP280_TEMP_OS_8
        self.bmp280_object.press_os = BMP280_TEMP_OS_4
        self.bmp280_object.standby = BMP280_STANDBY_250
        self.bmp280_object.iir = BMP280_IIR_FILTER_2

    def bmp_run(self):
        # accquire temperature value in celcius
        temperature_c = self.bmp280_object.temperature  # degree celcius

        # convert celcius to kelvin
        temperature_k = temperature_c + 273.15

        # accquire pressure value
        pressure = self.bmp280_object.pressure  # pascal

        # convert pascal to hectopascal (hPa)
        pressure_hPa = (pressure * 0.01) + self.ERROR  # hPa

        # accquire altitude values from HYPSOMETRIC formula
        h = altitude_HYP(pressure_hPa, temperature_k)

        # accquire altitude values from International Barometric Formula
        altitude = altitude_IBF(pressure_hPa)
        press = "{:.2f}".format(pressure_hPa)
        h_alti = "{:.2f}".format(h)
        i_alti = "{:.2f}".format(altitude)

        resp = f'{press}; {i_alti}; {h_alti}; {temperature_c};'
        return resp

