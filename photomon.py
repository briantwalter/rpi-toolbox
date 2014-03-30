#!/usr/bin/python
# 
# photomon.py
# 
# control the hdmi port based on values from a photocell
#
 
import RPi.GPIO as GPIO, time, os      
 
DEBUG = 1
GPIO.setmode(GPIO.BCM)
 
def RCtime (RCpin):
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        #time.sleep(0.1)
        time.sleep(0.5)
 
        GPIO.setup(RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading
 
while True:                                     
        print RCtime(22)     # Read RC timing using pin #22
