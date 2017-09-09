import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, filtfilt

highcut = 6.5
lowcut = 40
samplingf = 343.1
#Define the filter
def butter_lowpass(cutoff, samplef, order=5):
    nyq = 0.5 * samplef #Nyquist frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype = 'low', analog = False)
    return b, a

def butter_lowpass_filter(data, cutoff, samplef, order):
    b, a = butter_lowpass(cutoff, samplef , order = order)
    y = lfilter(b , a , data)
    return y

def butter_highpass(cutoff, fs, order):
    nyq = 0.5 * fs #A normalized frequency
    normal_cutoff = cutoff / nyq #A normalized frequency cutoff
    b, a = butter(order, normal_cutoff, btype = 'high', analog = False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order):
    b, a = butter_highpass(cutoff, fs, order)
    x = lfilter(b, a, data)
    return x

def butter_bandpass(low, high, fs, order=5):
    nyq = 0.5 * fs
    normlow = low/nyq
    normhigh = high/nyq
    b, a = butter(order, [normlow, normhigh], btype='band')
    return b, a

def butter_bandpass_filter(data, low, high, fs, order=5):
    b, a = butter_bandpass(low, high, fs, order = order)
    z = lfilter(b, a, data)
    return z

def butter_bandstop(low, high, fs, order):
    nyq = 0.5 * fs
    normlow = low/nyq
    normhigh = high/nyq
    b, a = butter(order, [normlow, normhigh], btype ='bandstop')
    return b, a

def butter_bandstop_filter(data, low, high, fs, order):
    b, a = butter_bandstop(low, high, fs, order)
    d = lfilter(b, a, data)
    return d

data = np.loadtxt('files/unipolardata3.txt')

#highfiltered = butter_highpass_filter(data, 0.5, samplingf, 1)
lowfiltered = butter_lowpass_filter(data, lowcut, samplingf, 5)
#bandfiltered = butter_bandpass_filter(data, lowcut, highcut, samplingf, 5)
#notchfiltered = butter_bandstop_filter(lowfiltered, 0.05, 0.06, samplingf, 1)

plt.subplot(211)
plt.plot(data, 'r-', label='ECG') # Point shape
plt.ylim(200,1000) #Bounds on the y axis
plt.title('Your ECG') #Title
plt.grid(False) #Activate Grid
plt.ylabel('ECG') #Y axis label
plt.legend(loc = 'upper right') # Legend
plt.ticklabel_format(useOffset=False) # Turn off autoscale

plt.subplot(212)
plt.plot(lowfiltered, 'b-', label = 'FilteredECG')
plt.ylim(200,1000)
plt.ticklabel_format(useOffset=False)

#plt.subplot(222)
#plt.plot(highfiltered, 'g-', label = 'HighFilteredECG')
#plt.ylim(200,1000)
#plt.ticklabel_format(useOffset=False)
#np.savetxt('files/filtereddata3.txt', lowfiltered)

plt.show()
