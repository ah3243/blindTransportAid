#!/usr/bin/env python

############################################################
###           Pi Opencv Colored Object locator           ###
############################################################
 
## This program is designed to look for objects in a video stream within a certain HSV range
## then calculate the distance of the nearest object to the centre, using this to control a 
## coin vibration motor through PWM. This is designed to be used on raspberry pi but can be
## used on a standard computer with static video files

#--- FLAGS ---#
# RUNNINGONPI = False # true if running on the pi
# ACTUATORSON = False # route signals to actuators
RUNNINGONPI = True # true if running on the pi
ACTUATORSON = True # route signals to actuators
VIDEOSTREAM = True # true if video stream being used from pi
TEST = False # only run a limited number of frames if true and display false

TUNEHSVRANGE = False # tune the target HSV range, with trackbar and target color area of image
DISPLAY = False # true if working from gui
VIDEOSAVE = False # if true save frames as video and output

## different methods of vibration escalation were investigated to determine which one 
## allowed for the fastest and most accurate handhold location
FEEDBACKTYPE = 2
# 1 == normal
# 2 == with 30 point jump in last 10% distance
# 3 == exponential increase
# 4 == melody



#--- IMPORTS ---#
# Opencv imports
import cv2
import numpy as np
import imutils

# utility to measure fps
from imutils.video import FPS

# python imports
from scipy.spatial import distance as dist # calculate pixel distance
import math # to calculate the maximum distance a certain actuator(actuators active area dimensions)

# module with general functions
import genUtils

# for audiomenu
import os

# various imports if running on pi
if RUNNINGONPI:
    # piCamera imports
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    import time
    # Raspberry Pi Actuator imports
    import RPi.GPIO as GPIO

# imports and initialisations depending on whether video or a camera stream are being used
if VIDEOSTREAM:
    from imutils.video.pivideostream import PiVideoStream
    vs = PiVideoStream().start()
    time.sleep(2.0)
else:
    inputVideo = "PostitNoteTests.avi"
    cap = cv2.VideoCapture(inputVideo)


#--- Definitions ---# 

# image dimensions

# ImgW = 800
# ImgH = 600

# ImgW = 640
# ImgH = 480

ImgW = 320
ImgH = 240


# distance range for objects
distMin = 0
distMax = 200

# PWM range for motors
MotorMin = 100
MotorMax = 0

### Actuator Initialisation ###
if ACTUATORSON and RUNNINGONPI:
    # pin numbers
    pin1 = 13 # motor1
    pin3 = 18 # motor2
    pin4 = 12 # motor3

    pin2 = 5 # used for start/stop button

    # motor config details
    ACCfreq = 200

    # choose pin numbering system
    GPIO.setmode(GPIO.BCM)

    # prevent Pi warning on startup
    GPIO.setwarnings(False)

    # set pins as output
    GPIO.setup(pin1, GPIO.OUT) # vibration motor
    GPIO.setup(pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # start/stop button

    # set PWM pins and frequency
    PWM_M1 = GPIO.PWM(pin1, ACCfreq)

    # initialise PWM values
    PWM_M1.start(0)

if DISPLAY:
    cv2.namedWindow('Normal')
    cv2.moveWindow('Normal', 700, 0)

def setTargetColor(x):
    global hul
    global huh
    global sal
    global sah
    global val
    global vah

    hsvVals = {
    "Black": [0, 255, 0, 20, 0,20], 
    "White" : [0, 255, 0, 30, 80, 100], 
    "Yellow" : [25, 219, 18, 43, 59, 255],
    "Orange" : [4, 21, 49, 255, 44, 255],
    "Blue" : [0, 253, 69, 124, 40, 255],
    "Pink" : [159, 179, 87, 255, 31, 255],
    "Stop": [0,0, 0, 0, 0, 0]
    }

    Cur = hsvVals[x]

    # val = Cur[0]
    # vah = Cur[1]
    # hul = Cur[2]
    # huh = Cur[3]
    # sal = Cur[4]
    # sah = Cur[5]
    
    hul = Cur[0]
    huh = Cur[1]
    sal = Cur[2]
    sah = Cur[3]
    val = Cur[4]
    vah = Cur[5]
    

# # HSV values for pink postit notes
# Black = [0, 255, 0, 20, 0,20] # value must be low, hue doesn't matter
# White = [0, 255, 0, 30, 80, 100] # saturation must be high here, hue again doesn't matter
# Yellow = [25, 219, 18, 43, 59, 255] # done with yellow/green postit note in shade
# Orange = [4, 21, 49, 255, 44, 255] # done with orange postit note in shade
# Blue = [0, 253, 69, 124, 40, 255] # done with a blue postit in shade
# Pink = [159, 179, 87, 255, 31, 255] # done with a pink postit in shade


hul, huh, sal, sah, val, vah = 0, 0, 0, 0, 0, 0
setTargetColor("Orange")

fps = FPS().start()

###
## Digital Encoder
###
RoAPin = 22    # pin11
RoBPin = 18    # pin12
RoSPin = 27  # pin13

## Define Search Area Variables
SearchRadius = 100 # search radius

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)    # input mode
    GPIO.setup(RoBPin, GPIO.IN)
    GPIO.setup(RoSPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    rotaryClear()
    print("Completed setup")

def rotaryDeal():
    global flag
    global Last_RoB_Status
    global Current_RoB_Status
    global SearchRadius

    dialIncrement = 4 # the amoung that the dial will increment the search area by
    SearchTop = ImgH
    SearchBottom = 20

    Last_RoB_Status = GPIO.input(RoBPin)

    while(not GPIO.input(RoAPin)):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            if (SearchRadius+dialIncrement<SearchTop):
                SearchRadius = SearchRadius + dialIncrement
                print('SearchRadius = {}'.format(SearchRadius))
                countTrack(True)
            else:
                print("Search radius too large cant increase")

        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            if(SearchRadius-dialIncrement>SearchBottom):
                SearchRadius = SearchRadius - dialIncrement
                print('SearchRadius = {}'.format(SearchRadius))
                countTrack(False)
            else: 
                print("Search radius too small cant decrease")

def clear(ev=None):
    SearchRadius = 100
    print('SearchRadius = {}'.format(SearchRadius))
    time.sleep(1)

def rotaryClear():
    GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) # wait for falling

## AudioMenu ##
mainMenu = [ "Pink", "Orange", "Black", "Stop"]
extension = ".mp3"
musicDir = "../Media/Audio/"
trackCount = 0 #used to track where the user is in the audio menu 

# count which track it is
def countTrack(direction):
    global trackCount
    global mainMenu
    if direction:
        trackCount+=1        
        if trackCount == len(mainMenu):
            trackCount =0
    elif(trackCount==0):
        trackCount = len(mainMenu)-1
    else:
        trackCount-=1

    playTrack()

# play the current track
def playTrack():
    global trackCount
    global mainMenu
    global musicDir

    print("currently track: {}".format(mainMenu[trackCount]))

    target = "mpg123 -C " + musicDir + mainMenu[trackCount] + extension
    print(target)
    os.system(target)
    setTargetColor(mainMenu[trackCount])

# def loop():
#     global SearchRadius
#     while True:
#         rotaryDeal()
#		print 'SearchRadius = %d' % SearchRadius

def destroy():
    print("keyboard interupt cleaning up")
    if(ACTUATORSON):    
        GPIO.cleanup()             # Release resource

    if(DISPLAY):
        cv2.destroyAllWindows()

    fps.stop()         # calculate fps values

###
##
###

count = 0 # to count the number of iterations in the loop
cont = False # flag for the stop/start button


if __name__ == '__main__':     # Program start from here
    setup()    
    try:
        # run the main loop
        while True:
            rotaryDeal()
            ### Actuator Initialisation ###
            if ACTUATORSON and RUNNINGONPI:	
                cont = GPIO.input(pin2)

            # continue if buttons pressed(if activated)
            # if cont==False:
            if True:
                if VIDEOSTREAM:
                    frame = vs.read()
                    frame = imutils.resize(frame, width=ImgW)
                    frame=cv2.flip(frame,-1)

                else:
                    #read the streamed frames (we previously named this cap)
                    (grabbed, frame) = cap.read()

                    # break when you get to the end of the video
                    if not grabbed:
                        break
                if count ==0:
                    height, width = frame.shape[:2]
                    ImgCentre = (int(width/2), int(height/2))

                # it is common to apply a blur to the frame
                frame=cv2.GaussianBlur(frame,(5,5),0)

                #convert from a BGR stream to an HSV stream
                hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                #make array for final values
                HSVLOW=np.array([hul,sal,val])
                HSVHIGH=np.array([huh,sah,vah])

                #create a mask for that range
                mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                res = cv2.bitwise_and(frame,frame, mask =mask)

                # find contours
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                # initialise (x,y) ball centre
                targetCenter = None

                # only proceed if at least one contour was found
                if len(cnts) > 0:
                    # find the largest contour
                    contour = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)

                    # calculate the contour centre
                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    targetCenter = (cX, cY)
                    
                    # # calculate the distance between the target and centre of the image
                    # Dist = int(dist.euclidean(ImgCentre, targetCenter))

                    # calculate the horizontal distance between the target and central vertical line
                    Dist = int(abs((ImgW/2)- cX))

                    if Dist < SearchRadius:
                        # print("within the bounds of the search radius")
                        # scale and invert the distance into a pwm value between 0-70(top 30 reserved for upper)
                        newVal = int(genUtils.getFeedbackVal(Dist, distMin, distMax, MotorMin, MotorMax, FEEDBACKTYPE))

                        print("The current distance between the target and centre is: {}, this is the translated value: {}".format(Dist, newVal))

                        # if running on pi then update vibration motor value
                        if RUNNINGONPI:
                            PWM_M1.start(newVal)
                        
                        if DISPLAY:
                            # draw circle to frame
                            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 100, 255), 2)
                            # draw centre point to frame
                            cv2.circle(frame, targetCenter, 5, (255, 0, 255), -1)

                            # display line from centre to target with width corresponding to distance
                            lineWidth = int(genUtils.translate(newVal, MotorMin, MotorMax, 20, 1))
                            cv2.line(frame, ImgCentre, targetCenter, (0,0,255),lineWidth)
                    else:
                        # print("not within the bounds of the search radius")

                        # if no target found then set motor to 0
                        if RUNNINGONPI:
                            PWM_M1.start(0)	                        
                else:
                    # if no target found then set motor to 0
                    if RUNNINGONPI:
                        PWM_M1.start(0)	

                # update the FPS counter
                fps.update()

                if DISPLAY:
                    # show the unmasked image
                    cv2.imshow("Normal", frame)

                    # show the masked colors in image		
                    cv2.imshow('Example', res)

                # if images displayed and q pressed then exit
                k = cv2.waitKey(1) & 0xFF

                # if images not displayed then exit after 1000 frames(for testing)
                count+=1
                if DISPLAY!=1 and TEST and count > 1000:
                    print("Test finished exiting")
                    break

            else:
                PWM_M1.start(0)	# set motor to zero if button not pressed
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.

        destroy()
        # display fps values
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))








