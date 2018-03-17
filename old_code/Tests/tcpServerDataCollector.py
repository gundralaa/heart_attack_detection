import os
import threading
import time

import Adafruit_ADS1x15
import numpy as np
import socket

GAIN = 1
TCP_IP = '10.0.0.68'
TCP_PORT = 5001
BUFFER_SIZE = 2
READ_TIME = 10
PORT_NUM = 1
SAMPLE_RATE = 256

adc = Adafruit_ADS1x15.ADS1015()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(TCP_IP,TCP_PORT)
s.listen(1)
conn, addr = s.accept()

while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data: break
	print "Status: ", data

start = time.time()
diff = time.time() - start

while (diff < READ_TIME):
	data = adc.read_adc(PORT_NUM, gain=GAIN, data_rate=SAMPLE_RATE)
	diff = time.time() - start
	conn.send(data)
conn.close()
