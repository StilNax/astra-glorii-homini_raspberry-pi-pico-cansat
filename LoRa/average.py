def coma_valid(value):
    if value[-1] == ',':
        return value[0:len(value) - 1]
    else:
        return value


def division(data):
    summary = sum(data)
    summary_str = str(summary)
    ext = len(summary_str) - 1 - summary_str.index(".")
    div = (int(summary_str.replace('.', '')) // len(data))
    data_resp = str(round(div / (10 ** ext), 2)) + ","
    return data_resp


def average(sensors_data_tmp):
    is_bmp = False
    is_bno = False

    bmp_lora_resp = ''
    bno_lora_resp = ''
    gps_lora_resp = ''

    press_list = []
    i_alti_list = []
    h_alti_list = []
    temperature_c_list = []
    bmp_list = [press_list, i_alti_list, h_alti_list, temperature_c_list]

    yaw_list = []
    pitch_list = []
    roll_list = []
    x_accel_list = []
    y_accel_list = []
    z_accel_list = []
    bno_list = [yaw_list, pitch_list, roll_list, x_accel_list, y_accel_list, z_accel_list]

    try:
        for package in sensors_data_tmp:
            if package[0] is not None and package[0] != "" and package[0] != "None":
                is_bmp = True
                resp = package[0]
                resp_list = resp.split(",")
                for x in range(len(resp_list)):
                    bmp_list[x].append(float(resp_list[x]))

            if package[1] is not None and package[1] != "" and package[1] != "None":
                is_bno = True
                resp = package[1]
                resp_list = resp.split(",")
                for x in range(len(resp_list)):
                    bno_list[x].append(float(resp_list[x]))

        if is_bmp:
            for bmp_data in bmp_list:
                bmp_lora_resp += division(bmp_data)
        else:
            bmp_lora_resp = "None,"
        if is_bno:
            for bno_data in bno_list:
                bno_lora_resp += division(bno_data)
        else:
            bno_lora_resp = "None,"

        sensors_data_tmp.reverse()
        gps_exist = False
        for package in sensors_data_tmp:
            if package[2] is not None and package[2][0:3] != "ERR":
                gps_lora_resp = package[2]
                gps_exist = True
                break
        if not gps_exist:
            gps_lora_resp = None

        bno_lora_resp = bno_lora_resp.replace("-0.009999999", "-0,01")
        bno_lora_resp = bno_lora_resp.replace("0.009999999", "0,01")

        sensors_data_tmp_new = str(coma_valid(bmp_lora_resp)) + ";" + str(coma_valid(bno_lora_resp)) + ";" + str(gps_lora_resp)

        return sensors_data_tmp_new
    except:
        return "None" + ";" + "None" + ";" + "None"
