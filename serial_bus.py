#serial_bus.py

import serial
import time
 
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.reset_input_buffer()
mileage = 0


def write(direction):
    ser.write((direction + '\n').encode())
            
def read():
    global mileage
    if ser.inWaiting() > 0:
        mileage = int(ser.readline().decode('UTF-8').strip())
    return mileage
