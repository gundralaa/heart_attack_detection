import numpy as np
import matplotlib as plt
import biosppy.signals.ecg as bio

def templateExtract(signal, rpeaks, sampling_rate, before_time, after_time):
    #Returns an array of single heart beats
    
    before = int(before_time * sampling_rate) #Change the times to samples
    after = int(after_time * sampling_rate)

    R = np.sort(rpeaks)
    length = len(signal)
    beats = []
    rlocation = []

    for r in R:
        a = r - before # Lower bound sample number
        if a < 0: # Lower then first sample
            continue
        b = r + after # Upper Bound sample number
        if b > length: # Greater then the total signal length
            break
        beats.append(signal[a:b]) # Add array with signal from lower to upper bound
        rlocation.append(r) # Get the r for the beat of that certain array

    beats = np.array(beats)
    rlocation = np.array(rlocation, dtype='int')

    return beats, rlocation

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
def classifyExtremal1(r, extrema):
    extrema = np.array(extrema)
    s = extrema.size()
    low = np.array([0])
    high = np.array([0])
    i = 0
    while(i <= s)
    e = extrema[i]
        if (e < r):
            np.append(low, e)
        elif (e > r):
            np.append(high, e)
    rev_low = low[::-1]
    rev_low

    return low,high