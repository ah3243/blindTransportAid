# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=1000,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())


# saving video code
vidSave = True
vidFPS = 30.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None
(h,w) = (None, None)
zeros = None

imgW = 1280
imgH = 920

#####
### Multi Thread!!
#####
# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream(resolution=(imgW, imgH)).start()
time.sleep(2.0)
fps = FPS().start()


cv2.namedWindow("Frame")

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of imgW pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=imgW)
 
	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	
	# update the FPS counter
	fps.update()
	
	if vidSave:
		if out is None:
			print("initialising video save var")
			(h, w) = frame.shape[:2]
			out = cv2.VideoWriter('output1.mp4', fourcc, vidFPS,(w, h), True)
		out.write(frame)

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
out.release() # release/save video
cv2.destroyAllWindows()
vs.stop()