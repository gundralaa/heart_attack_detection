import numpy as np
import matplotlib as plt
import biosppy.signals.ecg as bio

samplrate = 3428/10
data = np.loadtxt('FilteredData/filtereddata3.txt')

rpeaks1 = bio.christov_segmenter(data, 342)
bio.ecg(data, 342, True)
rpeaks2 = bio.engzee_segmenter(data, 342)
rpeaks3 = bio.gamboa_segmenter(data, 342)
rpeaks4 = bio.hamilton_segmenter(data, 342)
rpeaks5 = bio.ssf_segmenter(data, 342)

np.savetxt('FilteredData/peaksdata13.txt', rpeaks1, header=str(len(rpeaks1)))
np.savetxt('FilteredData/peaksdata23.txt', rpeaks2, header=str(len(rpeaks2)))
np.savetxt('FilteredData/peaksdata33.txt', rpeaks3, header=str(len(rpeaks3)))
np.savetxt('FilteredData/peaksdata43.txt', rpeaks4, header=str(len(rpeaks4)))
np.savetxt('FilteredData/peaksdata53.txt', rpeaks5, header=str(len(rpeaks5)))
#np.savetxt('FilteredData/roundeddata3.txt', introunddata)
