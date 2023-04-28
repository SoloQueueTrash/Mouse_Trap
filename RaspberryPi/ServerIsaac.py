#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time



if __name__ == '__main__':
    print('Server Running. Press CTRL-C to exit.')
    arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    arduino.flush() # flush any existing data in the input buffer
    time.sleep(0.1) #wait for serial to opens
    if arduino.isOpen():
        print("{} connected!".format(arduino.port))
        try:
            while True:
                cmd=input("Enter command : ") # Comando recebido da aplicação
                arduino.write(cmd.encode())
                #time.sleep(0.1) #wait for arduino to answer
                while arduino.inWaiting()==0: pass
                if  arduino.inWaiting()>0: 
                    answer=arduino.readline()
                    print(answer)
                    arduino.flushInput() #remove data after reading
        except KeyboardInterrupt:
            print("KeyboardInterrupt has been caught.")