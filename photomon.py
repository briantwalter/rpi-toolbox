#!/usr/bin/env python
# 
# photomon.py		HDMI control based on values from a photocell
# version		0.1.2
# author		Brian Walter @briantwalter
# description		Auto-shutoff the display based on ambient lighting
#
 
# imports
import datetime
import simplejson as json
import math
import os      
import requests
import time
import RPi.GPIO as GPIO
from daemon import runner
from ConfigParser import SafeConfigParser

# GPIO set up
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# grab configurations
config = SafeConfigParser()
config.read('photomon_conf.py')
hdmictl = config.get('photomon', 'hdmictl')
logfile = config.get('photomon', 'logfile')
pidfile = config.get('photomon', 'pidfile')

# turn on hdmi using a bash script
def hdmion():
    os.system("su - pi -c \"/bin/bash -l -c \'" + hdmictl + " on\'\"")

# turn off hdmi using a bash script
def hdmioff():
    os.system("su - pi -c \"/bin/bash -l -c \'" + hdmictl + " off\'\"")

# read values for the photocell
def readpin(readpin):
    # readpin config
    interval = config.getfloat('photomon', 'interval')
    gpiopin = config.getint('photomon', 'gpiopin')
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
    # get samples config
    samples = config.getint('photomon', 'samples')
    gpiopin = config.getint('photomon', 'gpiopin')
    sum = 0
    for n in range(0, samples):
        sum = sum + readpin(gpiopin)
    else:
        average = sum / samples
        return average

# simple timestamp for logs
def rightnow():
    now = datetime.datetime.now()
    return now

# define the main
def main():
    # get main configs
    totalloops = config.getint('photomon', 'totalloops')
    loratio = config.getfloat('photomon', 'loratio')
    hiratio = config.getfloat('photomon', 'hiratio')
    apiend = config.get('photomon', 'apiend')
    apikey = config.get('photomon', 'apikey')
    # start from a known state
    hdmioff()
    time.sleep(25)
    hdmion()
    # forever loop making sure the minimum samples have been collected
    while True:
        if totalloops > 0:
            time.sleep(5)
            oldaverage = newaverage
            newaverage = getaverage()
            payload = {'auth_token': apikey, 'current': newaverage, 'last': oldaverage}
            req = requests.post(apiend, data=json.dumps(payload))
            ratio = oldaverage / float(newaverage)
            now = rightnow()
            if ratio < loratio:
                print "INFO: turning off HDMI" + str(now)
                hdmioff()
            if ratio > hiratio:
                print "INFO: turning on HDMI" + str(now)
                hdmion()
            totalloops += 1
        else:
            newaverage = getaverage()
            totalloops += 1

# main app class
class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = logfile
        self.stderr_path = logfile
        self.pidfile_path = pidfile
        self.pidfile_timeout = 5
    def run(self):
        main()

# execute the app according to run time argument
app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
