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
