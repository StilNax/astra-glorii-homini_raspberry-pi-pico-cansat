import time
import _thread
import uasyncio

# import BNO libraries
from Sensors.BNO.bno08x_rvc_run import BNO_run

# import BMP libraries
from Sensors.BMP.bmp_run import BMP_run

# import SDcard libraries
from SDCard.sdcard_init import sdcard_init

# import GPS NEO 7M libraries
from Sensors.GPS_Neo7M.GPS_NEO_7M_run import GPS_NEO_7M_run

# import LoRa libraries
from LoRa.LoRaSender_run import LoRa_run
from LoRa.average import average

# import RGB diode libraries
from RGB_diode.diode_management import RGB_led

led = RGB_led()

try:
    # RGB diode initialization
    led.cyan()

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
except:
    led.red()
    while True:
        pass

# global variable to get access from different treat
sensors_data = ""
i = 0
j = 0
is_sending = False
start_time = time.time_ns()
gps_resp = ""


async def GPS_get():
    global gps_resp

    start_gps_time = time.time_ns()
    gps_resp = str(GPS_NEO_7M_object.gps7m_run())
    end_gps_time = time.time_ns()
    delay = 100 - ((end_gps_time - start_gps_time) * 0.000001)
    await uasyncio.sleep_ms(int(delay))


async def Sensors_management():
    global sensors_data
    global is_sending
    global start_time
    # global gps_resp
    i = 0
    j = 0
    k = 0
    sd_counter = 0
    tmp_sensor_data = ""
    is_sending = False
    led.blue()
    data_for_lora = []
    sensors_data_tmp = []
    now_ms = 0
    delay_ms = 0
    tmp_delay_ms = 0

    while True:
        if i >= 10:
            led.green()

        delay_start_time = time.time_ns()

        bmp_resp = str(BMP_object.bmp_run())
        bno_resp = str(BNO_object.bno_run())
        gps_resp = str(GPS_NEO_7M_object.gps7m_run())

        sensors_data = bmp_resp + ";" + bno_resp + ";" + gps_resp

        data_for_lora_tmp = [bmp_resp, bno_resp, gps_resp]
        data_for_lora.append(data_for_lora_tmp)

        if not is_sending:
            j += 1
            sensors_data_tmp = data_for_lora[:]
            data_for_lora.clear()
            LoRa_sender_thread = _thread.start_new_thread(LoRa_sender, (2, j, sensors_data_tmp, now_ms, tmp_delay_ms))
            is_sending = True
            tmp_delay_ms = 0

        end_time = time.time_ns()
        now_ms = int((end_time - start_time) * 0.000001)
        delay_ms = int((end_time - delay_start_time) * 0.000001)
        tmp_delay_ms += delay_ms
        tmp_sensor_data += str(i) + ";" + sensors_data + ";" + str(GPS_NEO_7M_object.msg) + ";" + str(now_ms) + ";" + str(delay_ms) + '\r\n'

        if sd_counter >= 13:
            k += 1
            # Create a file and write something to it
            with open("/sd/test01.txt", "a") as file:
                file.write(tmp_sensor_data)
            print(f"{k} add to SD card")
            tmp_sensor_data = ""
            sd_counter = 0

        i += 1
        sd_counter += 1

        await uasyncio.sleep_ms(40)


def LoRa_sender(id, j, sensors_data_tmp, now_ms, delay_ms):
    global is_sending

    LoRa_object.send(str(j) + ";" + average(sensors_data_tmp) + ";" + str(now_ms) + ";" + str(delay_ms))
    print(f'LoRa data have been send {j + 1} time')

    is_sending = False
    return


async def main():
    uasyncio.create_task(Sensors_management())

    while True:
        await GPS_get()


uasyncio.run(main())
