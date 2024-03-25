# On-board Python software for Astra Glorii Homini's CanSat based on Raspberry Pi Pico microcontroller board

The repository is included as a part of Design Review reports for
CanSat made by Astra Glorii Homini team.

The code is developed for Raspberry Pi Pico microcontroller board to control modules used for collecting
data during the mission. It makes use of multithreading mechanism. 


## Critical Design Review [CDR]

### - Update 0.1"

#### BMP280 sensor operation:
* sensors initialization using I2C communication protocol

``` python
class BMP_run:
    def __init__(self):
        # Defining BMP pinout and calibration

        # Caliberation error in pressure
        # it helps in calibrating altitude
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
```

* calculating and returning of temperature, pressure and altitude measurements

```python
def bmp_run(self):
    # accquire temperature value in celcius
    temperature_c = self.bmp280_object.temperature  # degree celcius

    # convert celcius to kelvin
    temperature_k = temperature_c + 273.15

    # accquire pressure value
    pressure = self.bmp280_object.pressure  # pascal
    pressure_hPa = (pressure * 0.01) + self.ERROR  # hPa

    # accquire altitude values from HYPSOMETRIC formula
    h = self.altitude_HYP(pressure_hPa, temperature_k)

    # accquire altitude values from International Barometric Formula
    altitude = self.altitude_IBF(pressure_hPa)
    press = "{:.2f}".format(pressure_hPa)
    h_alti = "{:.2f}".format(h)
    i_alti = "{:.2f}".format(altitude)

    resp = f'{press}; {i_alti}; {h_alti}; {temperature_c};'
    return resp
```

<br />

### - Update 0.2"
#### BNO085 sensor operation:
* sensors initialization using UART-RVC communication protocol
```python
def __init__(self):
    UARTid = 1         # named argument - id
    baudrate = 115200  # named argument - baudrate
    txPin = Pin(8)     # named argument - tx pin
    rxPin = Pin(9)     # named argument - rx pin

    self.bno_uart = UART(UARTid, baudrate, tx=txPin, rx=rxPin)
    self.rvc = BNO08x_RVC(self.bno_uart)
```
UART-RVC communication protocol is better than regular UART protocol as it can send data in the form of packages that are easier to use and enables better data management.
However, it is slower than other communication protocols. Thanks to calibration it won't have any undesirable effects on the efficiency of the program.


* reading data from BNO085 and converting it to more useful and easy to interpret data presentation  
```python
def bno_run(self):
    try:
        try:
            yaw, pitch, roll, x_accel, y_accel, z_accel = self.rvc.heading
            resp1 = ("{:.2f}; {:.2f}; {:.2f}"
                     .format(yaw, pitch, roll))
            resp2 = ("{:.2f}; {:.2f}; {:.2f}"
                     .format(x_accel, y_accel, z_accel))
            return f'{resp1}, {resp2}'
        except RVCReadTimeoutError:
            print("Unable to read BNO08x UART.")
        sleep(.1)
    except KeyboardInterrupt:
        print("\nCtrl-C pressed to exit.")
```

<br />

### - Update 0.3"
#### GPS NEO 7M sensor operation:
* sensors initialization using UART communication protocol

```python
def __init__(self):
    UARTid = 0       # named argument - id
    baudrate = 9600  # named argument - baudrate
    txPin = Pin(16)  # named argument - tx pin
    rxPin = Pin(17)  # named argument - rx pin

    self.gps_module = UART(UARTid, baudrate, tx=txPin, rx=rxPin)
```

* configuration of GPS output
```python
GPS_config(self.gps_module)
```
```python
def GPS_config(uart):
    data = [
            b'\xB5\x62\x06\x08\x06\x00\x64\x00\x01\x00\x01\x00\x7A\x12',                             # rate = 100ms
            b'\xB5\x62\x06\x01\x08\x00\xF0\x00\x00\x00\x00\x00\x00\x00\xFF\x23',                     # GGA = disabled
            b'\xB5\x62\x06\x01\x08\x00\xF0\x01\x00\x00\x00\x00\x00\x00\x00\x2A',                     # GLL = disabled
            b'\xB5\x62\x06\x01\x08\x00\xF0\x02\x00\x00\x00\x00\x00\x00\x01\x31',                     # GSA = disabled
            b'\xB5\x62\x06\x01\x08\x00\xF0\x03\x00\x00\x00\x00\x00\x00\x02\x38',                     # GSV = disabled
            b'\xB5\x62\x06\x01\x08\x00\xF0\x05\x00\x00\x00\x00\x00\x00\x04\x46',                     # VTG = disabled
            b'\xB5\x62\x06\x09\x0D\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\x00\x00\x17\x31\xBF'  # CFG = save
            ]

    for i in range(len(data)):
        uart.write(data[i])
```
The ```data``` list consisting of hex format ubx messages configures GPS settings listed in the comments.
Thus, GPS returns only RMC message type and increases the frequency of data receiving. 
Ubx messages are sent directly to GPS by UART communication protocol.

* managing data from GPS  
```python
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
```
The GPS data size must be as small as possible due to the necessity of optimization of the whole module message. 
To do that the data that is crucial to the missions is selected from RMC message (latitude, longitude, speed over the ground, date or magnetic variation in degrees). 
Moreover, this solution will help with transferring the data via LoRa radio module. 

<br />

### - Update 0.4"
#### SD card reader module operation:
* SD card reader module initialization using SPI communication protocol and mounting the ```/sd``` folder in Raspberry Pi Pico memory 
```python
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
```
* adding example data to ```test.txt``` file in order to test the solution
```python
tmp_sensor_data = "test data"
# Create a file and write something to it
with open("/sd/test01.txt", "a") as file:
    file.write(tmp_sensor_data)
print("add to SD card")
```

<br />

### - Update 0.5"
#### LoRa sx1278 radio module operation:
* LoRa radio module initialization and configuration using SPI communication protocol
```python
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
```
This solution includes the most accurate configuration that meets the requirements provides maximum data sending efficiency. 

* sending data via LoRa radio module
```python
def send(self, data):
    self.lora.println(data)
```

<br />

### - Update 0.6"
#### integration of all solutions into one ```main.py``` file with many library's:
* importing all crucial libraries 
```python
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
```
Thanks to object programing used all of the above solutions are included in ```main.py``` file as libraries.
Such approach makes the project easier to manage and develop.

* initialization of all sensors, SD card reader and LoRa radio module
```python
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
```
* reading data from sensors, saving it on SD card and launching ```LoRa_sender``` thread
```python
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
```
```tmp_sensor_data``` string used as a SD card buffer together with ```sd_counter``` counter limit the number of saving operations on the card. 
Furthermore, they enhance the capacity of sensors data reading.

* multithreading concept
```python
import _thread
```
This module includes a multithreading solution. 
It enables launching multiple functions in separate simultaneous tasks working on different CPU cores.   

* using multithreading mechanism
```python
if not is_sending:
        j += 1
        sensors_data_tmp = str(j) + " " + sensors_data
        LoRa_sender_thread = _thread.start_new_thread(LoRa_sender, (2, j, sensors_data_tmp))
        is_sending = True
```
The above instruction initializes a new thread every time ```LoRa_sender``` function ends transferring data via LoRa. 
The```is_sending``` flag shows that the ```LoRa_sender``` function has ended and can be recalled in a new thread again.
Furthermore, in this way using more cores than available (Raspberry Pi Pico has two cores) is prevented.
The multithreading solution is crucial to the  missions to maximize the amount of data received from sensors while at the same time send data via LoRa at constant frequency.

* sending data via LoRa radio module
```python
def LoRa_sender(id, j, sensors_data_tmp):
    global is_sending

    LoRa_object.send(sensors_data_tmp)
    print(f'LoRa data have been send {j + 1} time')

    is_sending = False
    return
```
```LoRa_sender``` function within one threat must be followed by a return statement which ends the functioning of ```Lora_sender``` as well as the thread in which it was called. 
But for this mechanism the multithreading solution would work in an unstable way.

<br />

### - Update 1.1"
#### usage of `uasyncio` library:
* asynchronism concept
```python
import uasyncio
```
Thanks to `uasyncio` library GPS module data can be read at a lower frequency than in case of other sensors, which is crucial taking into account the fact that GPS module inherently responses more rarely than other sensors.

* getting data from gps
```python
async def GPS_get():
    global gps_resp

    start_gps_time = time.time_ns()
    gps_resp = str(GPS_NEO_7M_object.gps7m_run())
    end_gps_time = time.time_ns()
    delay = 100 - ((end_gps_time - start_gps_time) * 0.000001)
    await uasyncio.sleep_ms(int(delay))
```
This function enables reading GPS module data in an asynchronous way. At the same time it slows down another reading by 100ms assuring stability and preventing overwriting. 

* acync inicjalization:
```python
async def main():
    uasyncio.create_task(Sensors_management())

    while True:
        await GPS_get()
```
On the first CPU core the program runs as two asynchronous elements: data reading from the sensors and date reading from the GPS module. 
The data is then transferred between the tasks and finally between the CPU cores.

<br />

### - Update 1.2"
#### diode management:
* diode colours concept
```python
class RGB_led:
    def __init__(self):
        # RGB diode pin initialization
        self.red_diode = Pin(15, Pin.OUT)
        self.green_diode = Pin(14, Pin.OUT)
        self.blue_diode = Pin(18, Pin.OUT)
```
The RGB diode is connected to three Raspberry Pi Pico logic pins which are defined as ```Pin.OUT```. It enables driving an output voltage to the chosen pins in order to acquire a specific colour:
```python
def purple(self):
    self.blue_diode.value(1)
    self.green_diode.value(0)
    self.red_diode.value(1)
```

* import class into `main.py`
```python
# import RGB diode libraries
from RGB_diode.diode_management import RGB_led

led = RGB_led()
```
Thanks to such a solution changing the colour of the diode is easy, clear and dynamic in the whole working process:  
```python
led.cyan()
```

<br />

### - Update 1.3"
#### averaging data sent by LoRa:
* averaging concept

Averaging several consecutive readings raises the credibility and accuracy of data reading. It is particularly crucial in the process of setting the trajectory of CanSat flight since the data which is being sent includes no noise which might cause variation or distortion obscuring the outcome.    
```python
LoRa_object.send(str(j) + ";" + average(sensors_data_tmp) + ";" + str(now_ms) + ";" + str(delay_ms))
```
Averaging data is also connected with changes in entering data to the second threat:
1. assigning a set of readings to data type list in order to facilitate data operation in later stages
    ```python
    data_for_lora_tmp = [bmp_resp, bno_resp, gps_resp]
    data_for_lora.append(data_for_lora_tmp)
    ```
2. solving object reference problem by copying the temporary list to a new list and then clearing the former
    ```python
    sensors_data_tmp = data_for_lora[:]
    data_for_lora.clear()
    ```

* `average.py` function operation

`average.py` function consists of several stages:
1. preparing the data to be averaged
   ```python
    resp = package[1]
    resp_list = resp.split(",")
    for x in range(len(resp_list)):
        bno_list[x].append(float(resp_list[x]))
    ```
   ```python
   resp = package[1]
   resp_list = resp.split(",")
   for x in range(len(resp_list)):
       bno_list[x].append(float(resp_list[x]))
   ```
2. averaging the data 
   ```python
    for bmp_data in bmp_list:
        bmp_lora_resp += division(bmp_data)
    ```
   ```python
    def division(data):
        summary = sum(data)
        summary_str = str(summary)
        ext = len(summary_str) - 1 - summary_str.index(".")
        div = (int(summary_str.replace('.', '')) // len(data))
        data_resp = str(round(div / (10 ** ext), 2)) + ","
        return data_resp
    ```
   The above element solves the problem the `thread` library has with dividing `float` data resulting in unstable functioning of the program.  
<br />
3. returning the averaged data together with validated GPS data
    ```python
    sensors_data_tmp_new = str(coma_valid(bmp_lora_resp)) + ";" + str(coma_valid(bno_lora_resp)) + ";" + str(gps_lora_resp)
    ```
   GPS validation process consists in finding the latest correct GPS data reading.
    ```python
    for package in sensors_data_tmp:
        if package[2] is not None and package[2][0:3] != "ERR":
            gps_lora_resp = package[2]
    ```