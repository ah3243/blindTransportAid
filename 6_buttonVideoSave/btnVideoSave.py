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
import RPi.GPIO as GPIO
import time
from datetime import datetime as Tme

GPIO_StartBtn = 24
GPIO_LED = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_StartBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP) # start recording or not
GPIO.setup(GPIO_LED, GPIO.OUT) # LED to show recording
# ~12-14FPS (saving video)
# imgW = 1280
# imgH = 920

# ~
imgW = 800
imgH = 600

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=False,
    help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=1,
    help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-d", "--display", type=int, default=-1, help="Add -d 1 to display the captured images")
args = vars(ap.parse_args())

if args["display"] == 1:
    print("video display activated ")
    cv2.namedWindow("Frame")


cnt= 1 # to initialise fps at start of button press

def finish():
    # do a bit of cleanup
    print("[INFO] saving video...")
    vs.stop()
    writer.release()
    cv2.destroyAllWindows()

    fps.stop() # calculate fps values
    # display fps values
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    time.sleep(2) # wait for 2 seconds for the video to save    


try:
    while(True):
        input_state = GPIO.input(GPIO_StartBtn)

        # start loop if button pressed
        if input_state==False:
            print('Button Pressed')

            # initialise fps at start of video loop
            if cnt:
                fps = FPS().start()
                cnt =0

            GPIO.output(GPIO_LED, GPIO.HIGH)

            # initialize the video stream and allow the camera
            # sensor to warmup
            print("[INFO] warming up camera...")
            vs = VideoStream(usePiCamera=1, resolution=(imgW, imgH)).start()
            time.sleep(2.0)

            # initialize the FourCC, video writer, dimensions of the frame, and
            # zeros array
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = None
            (h, w) = (None, None)
            zeros = None

            rootName = "TestVid"
            # curTime = '_'+ str(Tme.hour()) + '_' + str(Tme.minute()) + '_' + str(Tme.second())
            Tme = Tme.now()
            curTime = "_" + str(Tme.hour) + "-" + str(Tme.minute)
            # print("Hours: {}, Minutes: {}, Seconds: {}".format(Tme.hour(), Tme.minute(), Tme.second()))
            print("hours: {}, minutes: {}".format(Tme.now().hour, Tme.now().minute))

            extension = ".avi"

            vidName = rootName + curTime + extension
            print("This is the time now: {}\n This is the vidName: {}".format(curTime, vidName))

            defaultFps = 25
        
            # store the image dimensions, initialzie the video writer,
            # and construct the zeros array
            frame = vs.read()
            frame = imutils.resize(frame, width=imgW)
            (h, w) = frame.shape[:2]

            writer = cv2.VideoWriter(vidName, fourcc, defaultFps,
                (w, h), True)

            ## loop over frames from the video stream
            # num_frames = 100
            # for i in range(num_frames):
            while(True):

                # grab the frame from the video stream and resize it to have a
                # maximum width of x pixels
                frame = vs.read()
                frame = imutils.resize(frame, width=imgW)
            
                writer.write(frame)
                print("Frame size: {}, shape: {}".format(frame.size, frame.shape))

                if args["display"] == 1:
                    # show the frames
                    cv2.imshow("Frame", frame)

                # cv2.imshow("Output", output)
                key = cv2.waitKey(1) & 0xFF # give it time to process
            
                input_state = GPIO.input(GPIO_StartBtn)
                if input_state:
                    print('Button unPressed')
                    break
                
                # update the FPS counter
                fps.update()

            finish()

        GPIO.output(GPIO_LED, GPIO.LOW)

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.

    print("Keyboard interupt. Cleaning up GPIO pins and closing.")
    finish()

    GPIO.output(GPIO_LED, GPIO.LOW)
    GPIO.cleanup()
    time.sleep(2)