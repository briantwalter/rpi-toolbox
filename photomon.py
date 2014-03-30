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
samples = 10 	# number of loop iterations
interval = 5 	# in seconds or partial seconds
totalloops = 0	# total number of times this ran
loratio = .65	# tolerance for turing off hdmi
hiratio = 1.35	# tolerance for turning no hdmi
hdmictl = "/home/pi/rpi-toolbox/hdmictl"

# set up gpio
GPIO.setmode(GPIO.BCM)
 
# turn on hdmi using a bash script
def hdmion():
  os.system("su - pi -c \"/bin/bash -l -c \'" + hdmictl + " on\'\"")

# turn off hdmi using a bash script
def hdmioff():
  os.system("su - pi -c \"/bin/bash -l -c \'" + hdmictl + " off\'\"")

# read values for the photocell
def readpin(readpin):
    reading = 0
    GPIO.setup(readpin, GPIO.OUT)
    GPIO.output(readpin, GPIO.LOW)
    time.sleep(interval)
    GPIO.setup(readpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(readpin) == GPIO.LOW):
      reading += 1
    return reading
 
# getaverage for the number of samples
def getaverage():
  sum = 0
  for n in range(0, samples):
    sum = sum + readpin(gpiopin)
    #print "DEBUG: sum is " + str(sum)
  else:
    #print "DEBUG: total sum is " + str(sum)
    average = sum / samples
    #print "DEBUG: average is " + str(average)
    return average

# main

# start from a known state
hdmioff()
time.sleep(25)
hdmion()
# forever loop making sure the minimum samples have been collected
while True:
  if totalloops > 0:
    #print "DEBUG: totalloops " + str(totalloops)
    oldaverage = newaverage
    #print "DEBUG: oldaverage is " + str(oldaverage)
    newaverage = getaverage()
    #print "DEBUG: newaverage is " + str(newaverage)
    ratio = oldaverage / float(newaverage)
    #print "DEBUG: ratio is " + str(ratio)
    if ratio < loratio:
      hdmioff()
    if ratio > hiratio:
      hdmion()
    totalloops += 1
  else:
    #print "DEBUG: totalloops " + str(totalloops)
    newaverage = getaverage()
    #print "DEBUG: newaverage is " + str(newaverage)
    totalloops += 1
