#######
# based partially on this blog post: https://botforge.wordpress.com/2016/07/02/basic-color-tracker-using-opencv-python/
#######

#import the necessary packages
import cv2
import numpy as np
#'optional' argument is required for trackbar creation parameters
def nothing(x):
	pass
 
Playthrough = False

fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
thickness = 1


#Capture video from the stream
# cap = cv2.VideoCapture(0)
inputVideo = "PostitNoteTests.avi"
cap = cv2.VideoCapture(inputVideo)
cv2.namedWindow('Normal')
cv2.moveWindow('Normal', 700, 0)

if Playthrough!=True:
	cv2.namedWindow('Colorbars') #Create a window named 'Colorbars'
	cv2.namedWindow('Values')

	cv2.moveWindow('Colorbars', 20, 0)
	cv2.moveWindow('Values', 330, 0)


#assign strings for ease of coding
hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'
wnd = 'Colorbars'

## INDOOR CLIMBING
# values for pink (VL, VH, HL, HH, SL, SH)
Pink = [31, 255, 159, 179, 87, 255]
## POSTIT NOTES
# values for pink postit notes
Postit_Pink = [31, 255, 159, 179, 87, 255]

Cur = [] 
Cur= Pink

if Playthrough != True:
	#Begin Creating trackbars for each
	cv2.createTrackbar(hl, wnd,Cur[2],179,nothing)
	cv2.createTrackbar(hh, wnd,Cur[3],179,nothing)
	cv2.createTrackbar(sl, wnd,Cur[4],255,nothing)
	cv2.createTrackbar(sh, wnd,Cur[5],255,nothing)
	cv2.createTrackbar(vl, wnd,Cur[0],255,nothing)
	cv2.createTrackbar(vh, wnd,Cur[1],255,nothing)

if Playthrough==True:
	hul = Cur[2]
	huh = Cur[3]
	sal = Cur[4]
	sah = Cur[5]
	val = Cur[0]
	vah = Cur[1]

# create new white image
img = np.zeros((400,200,3), dtype=np.uint8)
img.fill(255)

#begin our 'infinite' while loop
while(1):
	#read the streamed frames (we previously named this cap)
	(grabbed, frame) = cap.read()

	# break when you get to the end of the video
	if not grabbed:
		break


	cv2.imshow("Normal", frame)

	while(True):

		# it is common to apply a blur to the frame
		frame=cv2.GaussianBlur(frame,(5,5),0)
	
		#convert from a BGR stream to an HSV stream
		hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		if Playthrough!=True:
			#read trackbar positions for each trackbar
			hul=cv2.getTrackbarPos(hl, wnd)
			huh=cv2.getTrackbarPos(hh, wnd)
			sal=cv2.getTrackbarPos(sl, wnd)
			sah=cv2.getTrackbarPos(sh, wnd)
			val=cv2.getTrackbarPos(vl, wnd)
			vah=cv2.getTrackbarPos(vh, wnd)

			img2 = img.copy()

			cv2.putText(img2,str(val),(100,20), fontFace, fontScale,(0,0,0),thickness,cv2.LINE_AA)
			cv2.putText(img2,str(vah),(100,55), fontFace, fontScale,(0,0,0),thickness,cv2.LINE_AA)
			cv2.putText(img2,str(hul),(100,85), fontFace, fontScale,(0,0,0),thickness,cv2.LINE_AA)
			cv2.putText(img2,str(huh),(100,115), fontFace, fontScale,(0,0,0),thickness,cv2.LINE_AA)
			cv2.putText(img2,str(sal),(100,145), fontFace, fontScale,(0,0,0),thickness,cv2.LINE_AA)
			cv2.putText(img2,str(sah),(100,175), fontFace, fontScale,(0,0,0),thickness,cv2.LINE_AA)

			cv2.imshow('Values', img2)

		#make array for final values
		HSVLOW=np.array([hul,sal,val])
		HSVHIGH=np.array([huh,sah,vah])
	
		#create a mask for that range
		mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
	
		res = cv2.bitwise_and(frame,frame, mask =mask)
		
		cv2.imshow(wnd, res)

		if Playthrough == True:
			k = cv2.waitKey(1) & 0xFF
			break
		else: 
			k = cv2.waitKey(1) & 0xFF

		if k == ord('n'):
			break
		elif k == ord('q'):
			cv2.destroyAllWindows()
			exit()
 
