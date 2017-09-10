import sqlite3

import Adafruit_ADS1x15


def log_values(ecg):
    conn = sqlite3.connect('projects/heart_attack_detection/lab_app.db')  # It is important to provide an
    # absolute path to the database
    # file, otherwise Cron won't be
    # able to find it!
    curs = conn.cursor()
    curs.execute("""INSERT INTO ECG values((datetime(CURRENT_TIMESTAMP, 'localtime'), (?))""", ecg)
    conn.commit()
    conn.close()

adc = Adafruit_ADS1x15.ADS1015()
ecg_data = adc.read_adc(1, data_rate=256)

if ecg_data is not None:
    log_values(ecg_data)
else:
    log_values(1024)



