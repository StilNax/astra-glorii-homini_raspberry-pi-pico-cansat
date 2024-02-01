# import time
# import pyRTOS
#
# # import BNO library's
# from Sensors.BNO.bno08x_rvc_run import BNO_run
#
# # import BMP library's
# from Sensors.BMP.bmp_run import BMP_run
# from SDCard.sdcard_init import sdcard_init
#
# # import GPS NEO 7M library's
# from Sensors.GPS_Neo7M.GPS_NEO_7M_run import GPS_NEO_7M_run
#
# # import LoRa library's
# from LoRa.LoRaSender_run import LoRa_run
#
# # BMP initialization
# BMP_object = BMP_run()
#
# # GPS initialization
# GPS_NEO_7M_object = GPS_NEO_7M_run()
#
# # BNO initialization
# BNO_object = BNO_run()
#
# # SDcard initialization
# sdcard_init()
#
# # LoRa initialization
# LoRa_object = LoRa_run()
#
# # # global variable to get access from different treat
# sensors_data = ""
# i = 0
#
#
# def Sensors_management(self):
#     global sensors_data
#     global i
#
#     yield
#
#     while True:
#         bmp_resp = str(BMP_object.bmp_run())
#         bno_resp = str(BNO_object.bno_run())
#         gps_resp = str(GPS_NEO_7M_object.gps7m_run())
#         yield
#
#         sensors_data = bmp_resp + " " + bno_resp + " " + gps_resp
#         yield
#
#         # Create a file and write something to it
#         with open("/sd/test01.txt", "a") as file:
#             file.write(f'{sensors_data}\r\n')
#         yield
#
#         print(f"added {i + 1} time, {sensors_data}")
#         i += 1
#         yield [pyRTOS.timeout(0.03)]
#
#
# def LoRa_sender(self):
#     global sensors_data
#     global i
#
#     yield
#
#     while True:
#         LoRa_object.send(str(i) + " " + sensors_data)
#         yield
#         print(f"{sensors_data}, {i + 1}")
#         yield [pyRTOS.timeout(0.03)]
#
#
# pyRTOS.add_task(pyRTOS.Task(LoRa_sender))
# pyRTOS.add_task(pyRTOS.Task(Sensors_management))
#
# pyRTOS.start()
# # import pyRTOS
# # import machine
# #
# #
# # def task25(self):
# #     ledpin28 = machine.Pin(25, machine.Pin.OUT)
# #     ledpin28.value(0)
# #     yield
# #
# #     while True:
# #         ledpin28.toggle()
# #         yield [pyRTOS.timeout(1.25)]
# #
# # pyRTOS.add_task(pyRTOS.Task(task25))
# #
# # pyRTOS.start()
#
# # import time
# # import uasyncio
# #
# # # import BNO library's
# # from Sensors.BNO.bno08x_rvc_run import BNO_run
# #
# # # import BMP library's
# # from Sensors.BMP.bmp_run import BMP_run
# # from SDCard.sdcard_init import sdcard_init
# #
# # # import GPS NEO 7M library's
# # from Sensors.GPS_Neo7M.GPS_NEO_7M_run import GPS_NEO_7M_run
# #
# # # import LoRa library's
# # from LoRa.LoRaSender_run import LoRa_run
# #
# # # BMP initialization
# # BMP_object = BMP_run()
# #
# # # GPS initialization
# # GPS_NEO_7M_object = GPS_NEO_7M_run()
# #
# # # BNO initialization
# # BNO_object = BNO_run()
# #
# # # SDcard initialization
# # sdcard_init()
# #
# # # LoRa initialization
# # LoRa_object = LoRa_run()
# #
# # # # global variable to get access from different treat
# # sensors_data = ""
# # i = 0
# #
# #
# # async def Sensors_management():
# #     global sensors_data
# #     global i
# #     bmp_resp = str(BMP_object.bmp_run())
# #     bno_resp = str(BNO_object.bno_run())
# #     gps_resp = str(GPS_NEO_7M_object.gps7m_run())
# #
# #     sensors_data = bmp_resp + " " + bno_resp + " " + gps_resp
# #
# #     # Create a file and write something to it
# #     with open("/sd/test01.txt", "a") as file:
# #         file.write(f'{sensors_data}\r\n')
# #
# #     print(f"added {i + 1} time, {sensors_data}")
# #
# #
# # async def LoRa_sender():
# #     global sensors_data
# #     global i
# #     LoRa_object.send(sensors_data)
# #     print(f"{sensors_data}, {i + 1}")
# #
# #
# # async def main():
# #     global i
# #     while True:
# #         await uasyncio.create_task(Sensors_management())
# #         uasyncio.create_task(LoRa_sender())
# #         i += 1
# #
# # uasyncio.run(main())
#
#
# # import uasyncio
# #
# # async def blink(led, period_ms):
# #     while True:
# #         led.on()
# #         await uasyncio.sleep_ms(5)
# #         led.off()
# #         await uasyncio.sleep_ms(period_ms)
# #
# # async def main(led1):
# #     uasyncio.create_task(blink(led1, 700))
# #     await uasyncio.sleep_ms(10_000)
# #
# # # Running on a generic board
# # from machine import Pin
# # uasyncio.run(main(Pin(25)))
#

import time
import _thread
import gc

# import BNO library's
from Sensors.BNO.bno08x_rvc_run import BNO_run

# import BMP library's
from Sensors.BMP.bmp_run import BMP_run

# import SDcard library's
from SDCard.sdcard_init import sdcard_init

# import GPS NEO 7M library's
from Sensors.GPS_Neo7M.GPS_NEO_7M_run import GPS_NEO_7M_run

# import LoRa library's
from LoRa.LoRaSender_run import LoRa_run

# BMP initialization
BMP_object = BMP_run()

# GPS initialization
GPS_NEO_7M_object = GPS_NEO_7M_run()

# BNO initialization
BNO_object = BNO_run()

# SDcard initialization
sdcard_init()

# LoRa initialization
LoRa_object = LoRa_run()

# global variable to get access from different treat
sensors_data = ""
i = 0
j = 0
is_sending = False
start_time = time.time_ns()


def Sensors_management():
    global sensors_data
    global is_sending
    global start_time
    i = 0
    j = 0
    sd_counter = 0
    tmp_sensor_data = ""
    is_sending = False
    # global lock

    while True:
        # lock.acquire()

        bmp_resp = str(BMP_object.bmp_run())
        bno_resp = str(BNO_object.bno_run())
        gps_resp = str(GPS_NEO_7M_object.gps7m_run())

        # print(f'BMP: {bmp_resp}')
        # print(f'BNO: {bno_resp}')
        # print(f'GPS: {gps_resp}')
        # print(f'BMP: {bmp_resp}, BNO: {bno_resp}')

        # with open("/sd/test01.txt", "rw+") as file:
        #     file.truncate()

        sensors_data = bmp_resp + " " + bno_resp + " " + gps_resp

        # print(f"{i + 1} {sensors_data}")

        if not is_sending:
            j += 1
            sensors_data_tmp = str(j) + " " + sensors_data
            LoRa_sender_thread = _thread.start_new_thread(LoRa_sender, (2, j, sensors_data_tmp))
            # LoRa_sender(2, j, sensors_data_tmp)
            is_sending = True

        # lock.release()

        # get time
        end_time = time.time_ns()
        now_ms = (end_time - start_time) * 0.000001

        if sd_counter >= 13:
            # Create a file and write something to it
            with open("/sd/test01.txt", "a") as file:
                file.write(tmp_sensor_data)
            print(f"{sd_counter + 1} add to SD card")
            tmp_sensor_data = ""
            sd_counter = 0

        tmp_sensor_data += str(i) + " " + sensors_data + " " + str(GPS_NEO_7M_object.msg) + " " + str(now_ms) + '\r\n'

        print(f"{i + 1} add")

        # print(sensors_data)

        i += 1
        sd_counter += 1

        time.sleep_ms(10)


def LoRa_sender(id, j, sensors_data_tmp):
    global is_sending
    # global j

    # start_time = time.time()
    LoRa_object.send(sensors_data_tmp)
    print(f'LoRa data have been send {j + 1} time')

    # end_time = time.time()

    # if end_time - start_time >= 1:
    #     is_sending = False
    #     return
    # else:
    #     # time.sleep(1 - (end_time - start_time))
    #     is_sending = False
    #     return
    is_sending = False
    return


# create a global lock
# lock = _thread.allocate_lock()

# LoRa_thread = _thread.start_new_thread(LoRa_sender, ())
# Sensors_management()

Sensors_management()
