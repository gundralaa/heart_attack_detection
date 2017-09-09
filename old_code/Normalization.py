from __future__ import division

import threading

import biosppy.signals.ecg as bio
import numpy as np

name = "Normalization Thread"


# basedrift = 20
# scalefactor =  0.3 / 60
# normalizefreq = 50 # This is the cuttoff frequency of the FFT

class normalThread(threading.Thread):
    """docstring for normalThread"""

    def __init__(self, filepath, name, basedrift, scalefactor, normalizefreq, rate):
        threading.Thread.__init__(self)
        self.name = name
        self.filepath = filepath
        self.basedrift = basedrift
        self.scalefactor = scalefactor
        self.normalizefreq = normalizefreq
        self.rate = rate

    def run(self):
        print "Starting" + name
        normalize(self.filepath, self.basedrift, self.scalefactor, self.normalizefreq)


def normalize(filepath, basedrift, scalefactor, normalizefreq, rate):
    data = np.loadtxt(filepath)
    beats = []
    templates = bio.ecg(data, rate, False)[4]
    for t in templates:
        beat = t
        beat -= basedrift
        beat *= scalefactor
        p = 20 * np.log10(np.abs(np.fft.rfft(beat)))  # FFT of the beat with a decibel scale
        nqf = rate / 2  # Calculates the nyquist frequency
        samps = len(p)  # Calculates the number of samples
        pperf = samps / nqf  # The number of points per frequency
        newpoints = int(pperf * normalizefreq)  # Calculates the number of points at a certain freqency
        s = np.array(p[0:newpoints])  # Appends the array
