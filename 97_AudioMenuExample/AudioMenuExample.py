#!/usr/bin/env python

###
## Partially Taken from https://www.sunfounder.com/learn/Super_Kit_V2_for_RaspberryPi/lesson-8-rotary-encoder-super-kit-for-raspberrypi.html
### on 13 july 2017

import RPi.GPIO as GPIO
import time

import os


RoAPin = 22    # pin11
RoBPin = 18    # pin12
RoSPin = 27  # pin13

globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

mainMenu = ["01_yellow.mp3", "02_red.mp3", "03_orange.mp3", "04_blue.mp3"]
musicDir = "../Media/Audio/"
count=0


def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)    # input mode
    GPIO.setup(RoBPin, GPIO.IN)
    GPIO.setup(RoSPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    rotaryClear()

# count which track it is
def countTrack(direction):
    global count
    if direction:
        count+=1        
        if count == len(mainMenu):
            count =0
    elif(count==0):
        count = len(mainMenu)-1
    else:
        count-=1

    playTrack()

# play the current track
def playTrack():
    global count

    print("current track: {}".format(mainMenu[count]))
    target = "mpg123 -C " + musicDir + mainMenu[count]
    print(target)
    os.system(target)

def rotaryDeal():
    global flag
    global Last_RoB_Status
    global Current_RoB_Status
    global globalCounter
    Last_RoB_Status = GPIO.input(RoBPin)
    while(not GPIO.input(RoAPin)):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0

        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            globalCounter = globalCounter + 1
            print('globalCounter = {}'.format(globalCounter))
            countTrack(True)
        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            globalCounter = globalCounter - 1
            print('globalCounter = {}'.format(globalCounter))
            countTrack(False)

def clear(ev=None):
    globalCounter = 0
    print('globalCounter = {}'.format(globalCounter))
    time.sleep(1)

def rotaryClear():
        GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear, bouncetime=200) # wait for falling

def loop():
    global globalCounter
    global count
    while True:
        rotaryDeal()
#        print 'globalCounter = %d' % globalCounter

def destroy():
    GPIO.cleanup()             # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()