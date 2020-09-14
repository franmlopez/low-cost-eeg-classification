# Backyard Brains Sep. 2019
# Made for python 3
# First install serial library
# Install numpy, pyserial, matplotlib
# pip3 install pyserial
#
# Code will read, parse and display data from BackyardBrains' serial devices
#
# Written by Stanislav Mircic
# stanislav@backyardbrains.com

import threading
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import socketio


global connected
connected = False
#change name of the port here
#port = 'COM4'
#port = '/dev/ttyUSB0'
port = '/dev/cu.usbserial-DO015D1O'
baud = 230400
global input_buffer
global sample_buffer
global dataframe
global cBufTail
cBufTail = 0
input_buffer = []
#sample_rate = 10000
#display_size = 30000 #3 seconds
sample_rate = 200
display_size = 600
sample_buffer = np.linspace(0,0,display_size)
serial_port = serial.Serial(port, baud, timeout=0)
last_time_recorded = 0
dataframe = np.array([0,0])


# Code updated with SocketIO
# First install SocketIO
# Written by Rodrigo Sanz Sep. 2020
# hola@rodrigosanz.com

sio = socketio.Client()
num = 0 

@sio.event
def connect():

    print('connection established')
    sio.emit('my event', {'data': 'Emit Test Event from here'})

@sio.event
def my_message(data):
    global num
    global dataframe
    global last_time_recorded

    print('message received with ', data)

    if data == "START SESSION":
        print("Reset Variables")
        last_time_recorded = 0
        dataframe = np.array([0,0])
    
    if data == "END SESSION":
        print("Saving CSV")
        num = num + 1
        strTemp = 'modulo' + str(num) + '.csv'
        np.savetxt(strTemp, dataframe, delimiter=',', header='time,data')

    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')


# End Code updated with SocketIO

# Original Code


def checkIfNextByteExist():
        global cBufTail
        global input_buffer
        tempTail = cBufTail + 1

        if tempTail==len(input_buffer):
            return False
        return True


def checkIfHaveWholeFrame():
        global cBufTail
        global input_buffer
        tempTail = cBufTail + 1
        while tempTail!=len(input_buffer):
            nextByte  = input_buffer[tempTail] & 0xFF
            if nextByte > 127:
                return True
            tempTail = tempTail +1
        return False;

def areWeAtTheEndOfFrame():
        global cBufTail
        global input_buffer
        tempTail = cBufTail + 1
        nextByte  = input_buffer[tempTail] & 0xFF
        if nextByte > 127:
            return True
        return False

def numberOfChannels():
    return 1

def handle_data(data):
    global input_buffer
    global cBufTail
    global sample_buffer
    global dataframe
    global last_time_recorded

    if len(data)>0:

        cBufTail = 0
        haveData = True
        weAlreadyProcessedBeginingOfTheFrame = False
        numberOfParsedChannels = 0

        while haveData:
            MSB  = input_buffer[cBufTail] & 0xFF

            if(MSB > 127):
                weAlreadyProcessedBeginingOfTheFrame = False
                numberOfParsedChannels = 0

                if checkIfHaveWholeFrame():

                    while True:

                        MSB  = input_buffer[cBufTail] & 0xFF
                        if(weAlreadyProcessedBeginingOfTheFrame and (MSB>127)):
                            #we have begining of the frame inside frame
                            #something is wrong
                            break #continue as if we have new frame

                        MSB  = input_buffer[cBufTail] & 0x7F
                        weAlreadyProcessedBeginingOfTheFrame = True
                        cBufTail = cBufTail +1
                        LSB  = input_buffer[cBufTail] & 0xFF

                        if LSB>127:
                            break #continue as if we have new frame

                        LSB  = input_buffer[cBufTail] & 0x7F
                        MSB = MSB<<7
                        writeInteger = LSB | MSB
                        numberOfParsedChannels = numberOfParsedChannels+1
                        if numberOfParsedChannels>numberOfChannels():

                            #we have more data in frame than we need
                            #something is wrong with this frame
                            break #continue as if we have new frame

                        this_sample = writeInteger-512
                        sample_buffer = np.append(sample_buffer, this_sample)
                        time_now = datetime.now().timestamp()
                        time_elapsed = float("{:.6f}".format(time_now-time_start))
                        
                        if (time_elapsed > last_time_recorded + 0.002):
                            dataframe = np.vstack((dataframe, [time_elapsed, this_sample]))
                            last_time_recorded = time_elapsed
                            #print("print")

                        #dataframe = np.vstack((dataframe, [time_elapsed, this_sample]))
                        #print(dataframe)

                        if areWeAtTheEndOfFrame():
                            break
                        else:
                            cBufTail = cBufTail +1
                else:
                    haveData = False
                    break
            if(not haveData):
                break
            cBufTail = cBufTail +1
            if cBufTail==len(input_buffer):
                haveData = False
                break


def read_from_port(ser):
    global connected
    global input_buffer
    while not connected:
        #serin = ser.read()
        connected = True

        while True:

           reading = ser.read(1024)
           if(len(reading)>0):
                reading = list(reading)
#here we overwrite if we left some parts of the frame from previous processing
#should be changed
                input_buffer = reading.copy()
                #print("len(reading)",len(reading))
                handle_data(reading)

           time.sleep(0.005)

thread = threading.Thread(target=read_from_port, args=(serial_port,))
time_start = datetime.now().timestamp()
thread.start()

xi = np.linspace(-display_size/sample_rate, 0, num=display_size)

#Plot values with matplotlib 

""" while True:
    plt.ion()
    plt.show(block=False)
    if(len(sample_buffer)>0):
        #i = len(sample_buffer)
        #print(len(sample_buffer))
        yi = sample_buffer.copy()
        yi = yi[-display_size:]
        #sample_buffer = sample_buffer[-display_size:]
        #print(sample_buffer)
        plt.clf()
        plt.ylim(-550, 550)
        plt.plot(xi, yi, linewidth=1, color='royalblue')
        plt.pause(0.001)
        time.sleep(0.08)
 """

sio.connect('http://localhost:5000')
#io.wait()
