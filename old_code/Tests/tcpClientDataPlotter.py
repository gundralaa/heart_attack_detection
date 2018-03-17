import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import biosppy.signals.tools as st
import numpy as np

TCP_IP = '10.0.0.69'
TCP_PORT = 5001
BUFFER_SIZE = 1024
CON_MESSAGE = "Connected"


style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))
s.send(CON_MESSAGE)
data = []
while True:
	while 1:
		point = s.recv(BUFFER_SIZE)
		if not point: break
		print "Status: ", point
	if not point: pass
	np.append(data, point)

#filtered, _, _ = st.filter_signal(signal=data,ftype='FIR', band='bandpass', order= int(0.3 * 256), frequency=[3,45],sampling_rate=256)
np.savetxt('', filtered)
s.close()
