#####
##  This program will take in a colored key with 5 distinct colors(4 of which change) and parse them 
##  into a command from a conversion dictionary 
####

# import the necessary packages
from __future__ import print_function
import numpy as np
import argparse
import cv2
import imutils
import time
from imutils.video import VideoStream
from imutils.video import FPS

# # Button imports
# from datetime import datetime as Tme
import datetime
import VisionModule
import VideoHandlingModule
import cmdDictionary
import speakText
from RPi import GPIO

# ~12-14FPS (saving video)
# imgW = 1280
# imgH = 920

# ~
imgW = 800
imgH = 600

## Flags
DISPLAY = True
SAVE = False

## Button press
sw = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)


if DISPLAY:
    print("video display activated ")
    cv2.namedWindow("Frame")
    # cv2.namedWindow("Mask")

cnt= 1 # to initialise fps at start of button press
try:
    while(True):

        # initialise fps at start of video loop
        if cnt:
            fps = FPS().start()
            cnt =0

        # initialize the video stream and allow the camera
        # sensor to warmup
        print("[INFO] Starting camera stream...")
        vs = VideoStream(usePiCamera=1, resolution=(imgW, imgH)).start()
        time.sleep(2.0)
    
        if SAVE:
            # store the image dimensions, initialzie the video writer,
            # and construct the zeros array
            writer = VideoHandlingModule.createVideoWriter(vs, imgW)

        ## loop over frames from the video stream
        while(True):

            # grab the frame from the video stream and resize it to have a
            # maximum width of x pixels
            frame = vs.read()
            
            frame=cv2.flip(frame,-1)
            
            frame = imutils.resize(frame, width=imgW)
            # print("Frame size: {}, shape: {}".format(frame.size, frame.shape))

            if SAVE:        
                writer.write(frame)
        
            #convert from a BGR stream to an HSV stream
            hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
          
            if DISPLAY:
                # show the frames
                # cv2.imshow("Frame", frame)
                # cv2.imshow("Output", output)
                key = cv2.waitKey(1) & 0xFF # give it time to process            

            # # confirm that the purple (bottom line), is a certain size(within a certain range) before proceeding
            message = ""
            message = VisionModule.findColor(hsv, DISPLAY)

            # if button pressed speak the current target key
            pushBtn = GPIO.input(sw)
            if pushBtn != 1:
                print("Button pressed")
                speakText.speakCurrent(message)

            ## work out what the arrangement of colors are
                # find line length and save
                   # find Hue of pixel which is above and perpendicular  to the line 0.8 from the left of line
                   # at distances of 0.3 and 0.8 of length of the line
                # find Hue of pixel which is above and perpendicular  to the line 0.2 from the left of line
                    # at distances of 0.3 and 0.8 of length of the line
                # save which colors are in which position as a 4 digit number(each digit being the index of the color found)
            
            ## Parse this arrangement into a key value
                # run it through the cmdDictionary class methods
            
            ## use Flite and python to verbalise the value pair to the identified key
                # send text value to speakText class which generates synthesised speech
            
            # update the FPS counter
            fps.update()

        VideoHandlingModule.finish(vs, writer, fps, SAVE)
        key = cv2.waitKey(1) & 0xFF

except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.

    print("Keyboard interupt. Cleaning up and closing.")
    VideoHandlingModule.finish(vs, fps, SAVE, writer=0)
    cv2.destroyAllWindows()
    time.sleep(2)