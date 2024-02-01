from time import sleep
from Sensors.BNO.bno08x_rvc import *
from machine import UART, Pin


class BNO_run:
    def __init__(self):
        UARTid = 1         # named argument - id
        baudrate = 115200  # named argument - baudrate
        txPin = Pin(8)     # named argument - tx pin
        rxPin = Pin(9)     # named argument - rx pin

        self.bno_uart = UART(UARTid, baudrate, tx=txPin, rx=rxPin)
        self.rvc = BNO08x_RVC(self.bno_uart)

    def bno_run(self):
        try:
            try:
                yaw, pitch, roll, x_accel, y_accel, z_accel = self.rvc.heading
                resp1 = ("{:.2f}; {:.2f}; {:.2f}"
                         .format(yaw, pitch, roll))
                resp2 = ("{:.2f}; {:.2f}; {:.2f}"
                         .format(x_accel, y_accel, z_accel))
                # print("--------------------------------------------")
                return f'{resp1}, {resp2}'
                # return yaw, pitch, roll, x_accel, y_accel, z_accel, res1, res2, res3
            except RVCReadTimeoutError:
                print("Unable to read BNO08x UART.")
            sleep(.1)
        except KeyboardInterrupt:
            print("\nCtrl-C pressed to exit.")
        # finally:
        #     self.uart.deinit()

    # def bno_run_tmp(self):
    #     return self.bno_uart.read(2)
