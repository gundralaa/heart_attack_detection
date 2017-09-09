import serial
import time
ser = serial.Serial("/dev/ttyACM0", 57600)
timestamp = time.asctime(time.localtime(time.time()))
datafile = open("files/"+timestamp+".txt","w")
print timestamp
time.sleep(5)
readtime = 10
start = time.time()
diff = time.time() - start
while (diff < readtime):
    data = ser.readline()
    datafile.write(data)
    diff = time.time() - start
print "done"

