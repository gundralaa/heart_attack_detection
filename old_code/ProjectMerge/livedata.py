import serial #import the Serial library

import numpy  #import numpy

import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *

ecgValue = [] #Array that will store our data
ser = serial.Serial("/dev/ttyACM0", 57600, timeout=None) #Serial Port open
cnt = 0 #The data point count
cnter = 0

def makeFig():
    plt.ylim(200,1000) #Bounds on the y axis
    plt.title('Your ECG') #Title
    plt.grid(True) #Activate Grid
    plt.ylabel('ECG') #Y axis label
    plt.plot(ecgValue, 'r-', label='ECG') # Point shape
    plt.legend(loc = 'upper right') # Legend
    plt.ticklabel_format(useOffset=False) # Turn off autoscale


while True: #Loops forever LOL
    while (ser.inWaiting() == 0):
        pass
    data = ser.readline() # Read the line
   # cnter = cnter + 1
    #if( cnter == 100 ):
    floatdata = float( data ) # Take the data and convert to int
    ecgValue.append(floatdata) # Build the array
    drawnow(makeFig) # Make the figure
    plt.pause(0.000001) # Pause to prevent crash
    #    cnter = 0
    cnt=cnt+1 # Add to the point count
    if(cnt>50):  #Change to display more points 
        ecgValue.pop(0) # If more then 100 points shown then pop the first element in the array
