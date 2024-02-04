import time
import _thread
from machine import Pin

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
diode = Pin(15, Pin.OUT)


def Sensors_management():
    global sensors_data
    global is_sending
    global start_time
    i = 0
    j = 0
    sd_counter = 0
    tmp_sensor_data = ""
    is_sending = False
    diode.value(1)

    while True:
        bmp_resp = str(BMP_object.bmp_run())
        bno_resp = str(BNO_object.bno_run())
        gps_resp = str(GPS_NEO_7M_object.gps7m_run())

        sensors_data = bmp_resp + " " + bno_resp + " " + gps_resp

        if not is_sending:
            j += 1
            sensors_data_tmp = str(j) + " " + sensors_data
            LoRa_sender_thread = _thread.start_new_thread(LoRa_sender, (2, j, sensors_data_tmp))
            is_sending = True

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

        i += 1
        sd_counter += 1

        time.sleep_ms(100)


def LoRa_sender(id, j, sensors_data_tmp):
    global is_sending

    LoRa_object.send(sensors_data_tmp)
    print(f'LoRa data have been send {j + 1} time')

    is_sending = False
    return


Sensors_management()
