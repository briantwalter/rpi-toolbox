#!/usr/bin/python
# 
# photomon.py
# 
# control the hdmi port based on values from a photocell
#
 
import os      
import time
import math
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# debug settings
DEBUG = 1
# configuration variables
gpiopin = 22	# gpio pin on the rpi
samples = 4 	# number of loop iterations
interval = 1 	# in seconds or partial seconds
hdmictl = "/home/pi/rpi-toolbox/hdmictl"

# start at a known state and turn on the hdmi
os.system("su - pi -c \"" + hdmictl + " on\"")

GPIO.setmode(GPIO.BCM)
 
def readpin (readpin):
    reading = 0
    GPIO.setup(readpin, GPIO.OUT)
    GPIO.output(readpin, GPIO.LOW)
    time.sleep(interval)
    GPIO.setup(readpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(readpin) == GPIO.LOW):
      reading += 1
    return reading
 
def getaverage ():
  sum = 0
  for n in range(0, samples):
    sum = sum + readpin(gpiopin)
    print "DEBUG: sum is " + str(sum)
  else:
    print "DEBUG: total sum is " + str(sum)
    average = sum / samples
    print "DEBUG: average is " + str(average)
    return average

newaverage = getaverage()
print "DEBUG: newaverage is " + str(newaverage)




