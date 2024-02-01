def altitude_HYP(hPa, temperature):
    # Hypsometric Equation (Max Altitude < 11 Km above sea level)
    temperature = temperature
    local_pressure = hPa
    sea_level_pressure = 1013.25  # hPa
    pressure_ratio = sea_level_pressure / local_pressure  # sea level pressure = 1013.25 hPa
    h = (((pressure_ratio ** (1 / 5.257)) - 1) * temperature) / 0.0065
    return h


# altitude from international barometric formula, given in BMP 180 datasheet
def altitude_IBF(pressure):
    local_pressure = pressure  # Unit : hPa
    sea_level_pressure = 1013.25  # Unit : hPa
    pressure_ratio = local_pressure / sea_level_pressure
    altitude = 44330 * (1 - (pressure_ratio ** (1 / 5.255)))
    return altitude
