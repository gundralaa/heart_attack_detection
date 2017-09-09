# Libraries
import os
import time

import biosppy.signals.tools as st
import numpy as np
import serial

# Directory Preperations
timestamp = time.asctime(time.localtime(time.time()))
path = "/home/abhinav/projects/ECG_Development/MainCode/" + timestamp
os.makedirs(path)
ser = serial.Serial("/dev/ttyACM0", 57600)
readtime = 10
counter = 0
basedrift = 20
scalefactor = 0.3 / 60

time.sleep(5)
# Main Loop
'''
Creates 6 different 10 Second samples
that are completely filtered and normalized
for spectral analysis
'''
while (counter < 6):
    # Data File Read
    data = []
    filepath = path + "/" + str(counter) + ".txt"
    # datafile = open( filepath ,"w")
    start = time.time()
    diff = time.time() - start
    # 10 Sec Loop Through
    while (diff < readtime):
        line = ser.readline()
        # datafile.write(data)
        np.append[data, line]
        diff = time.time() - start
    # datafile.close()

    # Numpy Array Creation
    # data = np.loadtxt(filepath)
    samplrate = (data.size) / 10.0
    samplrate = float(samplrate)

    # Powerline Interference Frequency Filter
    lowfiltered = butter_lowpass_filter(data, lowcut, samplingf, 5)

    # Filter Signal For Smoothing
    order = int(0.3 * samplrate)
    filtered, _, _ = st.filter_signal(signal=lowfiltered,
                                      ftype='FIR',
                                      band='bandpass',
                                      order=order,
                                      frequency=[3, 45],
                                      sampling_rate=samplrate)
    # Normalization
    filtered -= basedrift
    filtered *= scalefactor

    # Save to TXT file
    np.savetxt(filepath, filtered)
    counter = counter + 1


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
