# def bmp_run_def(bmp280_object, ERROR):
#     # Function for calculation altitude from pressure and temperature values
#     # because altitude() method is not present in the Library
#
#     def altitude_HYP(hPa, temperature):
#         # Hypsometric Equation (Max Altitude < 11 Km above sea level)
#         temperature = temperature
#         local_pressure = hPa
#         sea_level_pressure = 1013.25  # hPa
#         pressure_ratio = sea_level_pressure / local_pressure  # sea level pressure = 1013.25 hPa
#         h = (((pressure_ratio ** (1 / 5.257)) - 1) * temperature) / 0.0065
#         return h
#
#     # altitude from international barometric formula, given in BMP 180 datasheet
#     def altitude_IBF(pressure):
#         local_pressure = pressure  # Unit : hPa
#         sea_level_pressure = 1013.25  # Unit : hPa
#         pressure_ratio = local_pressure / sea_level_pressure
#         altitude = 44330 * (1 - (pressure_ratio ** (1 / 5.255)))
#         return altitude
#
#     # accquire temperature value in celcius
#     temperature_c = bmp280_object.temperature  # degree celcius
#
#     # convert celcius to kelvin
#     temperature_k = temperature_c + 273.15
#
#     # accquire pressure value
#     pressure = bmp280_object.pressure  # pascal
#
#     # convert pascal to hectopascal (hPa)
#     # 1 hPa = 100 Pa
#     # Therefore 1 Pa = 0.01 hPa
#     pressure_hPa = (pressure * 0.01) + ERROR  # hPa
#
#     # accquire altitude values from HYPSOMETRIC formula
#     h = altitude_HYP(pressure_hPa, temperature_k)
#
#     # accquire altitude values from International Barometric Formula
#     altitude = altitude_IBF(pressure_hPa)
#     press = "{:.2f}".format(pressure_hPa)
#     h_alti = "{:.2f}".format(h)
#     i_alti = "{:.2f}".format(altitude)
#     # print("Temperature : ", temperature_c, " Degree Celcius")
#     # print("Pressure : ", pressure, " Pascal (Pa)")
#     # print("Pressure : ", press, " hectopascal (hPa) or millibar (mb)")
#     # print("Altitude (Hypsometric Formula) : ", h_alti, " meter")
#     # print("Altitude (International Barometric Formula) : ", i_alti, " meter")
#     # print("\n")
#
#     resp = f'{temperature_c}, {pressure}, {press}, {h_alti}, {i_alti}'
#
#     return resp

from Sensors.BMP.bmp280 import *
from Sensors.BMP.bmp_calculation_methods import altitude_HYP, altitude_IBF
from machine import I2C, Pin


class BMP_run:
    def __init__(self):
        # Defining BMP pinout and calibration

        # Caliberation error in pressure
        # use it according to your situation
        # it helps in calibrating altitude .It is optional, else put ERROR = 0
        self.ERROR = -3  # hPa

        I2C_id = 1        # positional argument - I2C id
        sclPin = Pin(27)  # named argument - serial clock pin
        sdaPin = Pin(26)  # named argument - serial data pin
        freq = 1000000    # named argument - i2c frequency

        # Initiate I2C
        bmp_i2c_object = I2C(I2C_id, scl=sclPin, sda=sdaPin, freq=freq)

        # scan i2c port for available devices
        # result = I2C.scan(bmp_i2c_object)
        # print("I2C scan result : ", result)  # 118 in decimal is same as 0x76 in hexadecimal

        # create a BMP 280 object
        self.bmp280_object = BMP280(bmp_i2c_object,
                                    addr=0x76,  # change it
                                    use_case=BMP280_CASE_WEATHER)

        # configure the sensor
        # These configuration settings give most accurate values in my case
        # tweak them according to your own requirements

        self.bmp280_object.power_mode = BMP280_POWER_NORMAL
        self.bmp280_object.oversample = BMP280_OS_HIGH
        self.bmp280_object.temp_os = BMP280_TEMP_OS_8
        self.bmp280_object.press_os = BMP280_TEMP_OS_4
        self.bmp280_object.standby = BMP280_STANDBY_250
        self.bmp280_object.iir = BMP280_IIR_FILTER_2

    # Function for calculation altitude from pressure and temperature values
    # because altitude() method is not present in the Library

    # @staticmethod
    # def altitude_HYP(hPa, temperature):
    #     # Hypsometric Equation (Max Altitude < 11 Km above sea level)
    #     temperature = temperature
    #     local_pressure = hPa
    #     sea_level_pressure = 1013.25  # hPa
    #     pressure_ratio = sea_level_pressure / local_pressure  # sea level pressure = 1013.25 hPa
    #     h = (((pressure_ratio ** (1 / 5.257)) - 1) * temperature) / 0.0065
    #     return h
    #
    # # altitude from international barometric formula, given in BMP 180 datasheet
    # @staticmethod
    # def altitude_IBF(pressure):
    #     local_pressure = pressure  # Unit : hPa
    #     sea_level_pressure = 1013.25  # Unit : hPa
    #     pressure_ratio = local_pressure / sea_level_pressure
    #     altitude = 44330 * (1 - (pressure_ratio ** (1 / 5.255)))
    #     return altitude

    def bmp_run(self):
        # accquire temperature value in celcius
        temperature_c = self.bmp280_object.temperature  # degree celcius

        # convert celcius to kelvin
        temperature_k = temperature_c + 273.15

        # accquire pressure value
        pressure = self.bmp280_object.pressure  # pascal

        # convert pascal to hectopascal (hPa)
        # 1 hPa = 100 Pa
        # Therefore 1 Pa = 0.01 hPa
        pressure_hPa = (pressure * 0.01) + self.ERROR  # hPa

        # accquire altitude values from HYPSOMETRIC formula
        h = altitude_HYP(pressure_hPa, temperature_k)

        # accquire altitude values from International Barometric Formula
        altitude = altitude_IBF(pressure_hPa)
        press = "{:.2f}".format(pressure_hPa)
        h_alti = "{:.2f}".format(h)
        i_alti = "{:.2f}".format(altitude)

        # print("Temperature : ", temperature_c, " Degree Celcius")
        # print("Pressure : ", pressure, " Pascal (Pa)")
        # print("Pressure : ", press, " hectopascal (hPa) or millibar (mb)")
        # print("Altitude (Hypsometric Formula) : ", h_alti, " meter")
        # print("Altitude (International Barometric Formula) : ", i_alti, " meter")
        # print("\n")

        # resp = f'{temperature_c}, {pressure}, {press}, {h_alti}, {i_alti}'
        resp = f'{press}; {i_alti}; {h_alti}; {temperature_c};'
        return resp

