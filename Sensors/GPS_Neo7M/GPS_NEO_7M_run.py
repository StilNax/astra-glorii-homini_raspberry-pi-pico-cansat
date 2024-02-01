from machine import UART, Pin
from Sensors.GPS_Neo7M.GPS_NEO_7M_config import GPS_config


class GPS_NEO_7M_run:
    def __init__(self):
        UARTid = 0       # named argument - id
        baudrate = 9600  # named argument - baudrate
        txPin = Pin(16)  # named argument - tx pin
        rxPin = Pin(17)  # named argument - rx pin

        self.gps_module = UART(UARTid, baudrate, tx=txPin, rx=rxPin)

        # Configurate GPS output
        GPS_config(self.gps_module)

    def gps7m_run(self):
        self.gps_module.readline()
        self.msg = str(self.gps_module.readline())

        resp = None
        try:
            if self.msg is not None and self.msg.startswith("b'$GPRMC"):
                tmp_gps_resp = self.msg[self.msg.rindex("GPRMC") + 6:len(self.msg)]
                parts = tmp_gps_resp.split(',')
                if len(parts) >= 10:
                    resp = (parts[0] + ","
                            + parts[2] + ","
                            + parts[3] + ","
                            + parts[4] + ","
                            + parts[5] + ","
                            + parts[6] + ","
                            + parts[9] + ","
                            + parts[10])
            return str(resp)
        except:
            return "ERROR! " + self.msg
