import sqlite3

import Adafruit_ADS1x15

var = 1


def log_values(ecg):
    conn = sqlite3.connect('ecg_data.db')  # It is important to provide an
    # absolute path to the database
    # file, otherwise Cron won't be
    # able to find it!
    curs = conn.cursor()
    print(ecg)
    print(type(ecg))
    curs.execute("insert into ECG values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (ecg,))
    conn.commit()
    conn.close()


while var == 1:

    adc = Adafruit_ADS1x15.ADS1015()
    ecg_data = adc.read_adc(1, data_rate=250)

    if ecg_data is not None:
        log_values(ecg_data)
    else:
        log_values(1024)
