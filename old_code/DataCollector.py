1import os
import threading
import time

import Adafruit_ADS1x15
import numpy as np

name = "Data Collector Thread"

path = "/home/abhinav/projects/ECG_Development/MainCode/"


# Or create an ADS1015 ADC (12-bit) instance.
# adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
# adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.


def data_reader(read_time, file_path, low_cut, high_cut):
    GAIN = 1

    adc = Adafruit_ADS1x15.ADS1015()

    timestamp = time.asctime(time.localtime(time.time()))

    path = file_path + timestamp
    os.makedirs(path)

    readtime = 10
    counter = 0
    portnum = 1
    samplrate = 256

    while True:
        # Data File Read
        data = []
        filepath = path + "/" + str(counter) + ".txt"
        # datafile = open( filepath ,"w")
        start = time.time()
        diff = time.time() - start
    # 10 Sec Loop Through
    while (diff < readtime):
        line = adc.read_adc(portnum, gain=GAIN, data_rate=samplrate)
        # datafile.write(data)
        np.append[data, line]
        diff = time.time() - start
    # datafile.close()

    # Numpy Array Creation
    # data = np.loadtxt(filepath)

    # Powerline Interference Frequency Filter
    # lowfiltered = butter_lowpass_filter(data, lowcut, samplingf, 5)

    # Filter Signal For Smoothing
    order = int(0.3 * samplrate)
    # Apply a notch filter for powerline interference noise
    filtered, _, _ = st.filter_signal(signal=lowfiltered,
                                      ftype='FIR',
                                      band='bandstop',
                                      order=order,
                                      frequency=[lowcut, highcut],
                                      sampling_rate=samplrate)
    # Normalization
    # filtered -= basedrift
    # filtered *= scalefactor

    # Save to TXT file
    np.savetxt(filepath, filtered)


# Low pass filter functions
def butter_lowpass(cutoff, samplef, order=5):
    nyq = 0.5 * samplef  # Nyquist frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, samplef, order):
    b, a = butter_lowpass(cutoff, samplef, order=order)
    y = lfilter(b, a, data)
    return y
