# import the necessary packages
from __future__ import print_function
import numpy as np
import argparse
import cv2
import imutils
import time
from imutils.video import VideoStream

# # Button imports
import RPi.GPIO as GPIO
import time
from datetime import datetime as Tme

GPIO_StartBtn = 6
GPIO_LED = 26
GPIO_VibrationMotor = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_StartBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP) # start recording or not
GPIO.setup(GPIO_LED, GPIO.OUT) # LED to show recording
#GPIO.setup(GPIO_VibrationMotor, GPIO.OUT) # PWM for vibration motor


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

# for c in range(1):
while(True):
	input_state = GPIO.input(GPIO_StartBtn)
	if input_state == False:
		print('Button Pressed')

		GPIO.output(GPIO_LED, GPIO.HIGH)

		# initialize the video stream and allow the camera
		# sensor to warmup
		print("[INFO] warming up camera...")
		vs = VideoStream(usePiCamera=1).start()
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
		frame = imutils.resize(frame, width=300)
		(h, w) = frame.shape[:2]

		writer = cv2.VideoWriter(vidName, fourcc, defaultFps,
			(w, h), True)

		## loop over frames from the video stream
		# num_frames = 100
		# for i in range(num_frames):
		while(True):

			# grab the frame from the video stream and resize it to have a
			# maximum width of 300 pixels
			frame = vs.read()
			frame = imutils.resize(frame, width=300)
		
			writer.write(frame)
			print("Frame size: {}, shape: {}".format(frame.size, frame.shape))

			if args["display"] == 1:
				# show the frames
				cv2.imshow("Frame", frame)

			# cv2.imshow("Output", output)
			key = cv2.waitKey(1) & 0xFF
		
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

			input_state = GPIO.input(GPIO_StartBtn)
			if input_state == True:
				print('Button unPressed')
				break
		
		# do a bit of cleanup
		print("[INFO] saving video...")
		vs.stop()
		writer.release()
		cv2.destroyAllWindows()
		cv2.waitKey(2000)
	
	GPIO.output(GPIO_LED, GPIO.LOW)

	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

print("Cleaning up GPIO pins and closing.")
GPIO.cleanup()