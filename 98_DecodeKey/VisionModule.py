import time
import cv2
import numpy as np
import math

# values for pink (VL, VH, HL, HH, SL, SH)
OPEN = [0, 255, 0, 180, 0, 255]
#target colors
Purple = [36, 189, 172, 179, 26, 251] # the distinctive purple color

Cur = Purple
## assign variables
hul = Cur[2]
huh = Cur[3]
sal = Cur[4]
sah = Cur[5]
val = Cur[0]
vah = Cur[1]

def findPurpleLine(frame, DISPLAY):
    """find the purple line within the image and return length and xy values"""
    processTime = {}
    processTime = timeAction(processTime, "start", 0)

    lineDems = {
        "start": [0,0],
        "end": [0,0],
        "length": 0
        }
    findColor(frame, DISPLAY)

    timeAction(processTime, "end", "findPurple")
    return lineDems


def findColor(frame, DISPLAY):
    """ return the coordinates of a specific color in an image """
    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])

    # it is common to apply a blur to the frame
    frame=cv2.GaussianBlur(frame,(5,5),0)

    #create a mask for that range
    mask = cv2.inRange(frame,HSVLOW, HSVHIGH)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    if DISPLAY:
        # show the frames
        cv2.imshow("Frame2", mask)
        key = cv2.waitKey(1) & 0xFF # give it time to process            
    findPurpleDems(mask, frame)
    
    # res = cv2.bitwise_and(frame,frame, mask =mask)

def findPurpleDems(mask, frame):
    # find contours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    # only continue if there is at least one contour
    if len(cnts) > 0:
        # find the largest contour
        contour = max(cnts, key=cv2.contourArea)

        # find the smallest bounding rectangle, it's size position and orientation

        #  rect == ((x,y), (width, height), angle)
        rect = cv2.minAreaRect(contour)            

        # print("This is the x {}, y {}".format(x,y))
        # print("This is the width {}, height {}, angle {}".format(width, height, angle))


        # lineStart = int(x-(length/2))
        # lineEnd = int(x+(length/2))
        # # print("This is the length {}, height {}, Lstart {}, Lend {}".format(length, height, lineStart, lineEnd))

        # X = int(x)
        # Y = int(y)
        # cv2.line(frame,(lineStart,Y),(lineEnd,Y),(255,0,0),4)
        # cv2.circle(frame,(X,Y), 63, (0,0,255), -1)

        box = cv2.boxPoints(rect)
        print("box: {}".format(box[0]))

        # get the longest top side of the rectangle
        (sta,fin) = findTopRectSide(box)
        (sx, sy) = box[sta]
        (ex, ey) = box[fin]
        # print(start, finish)
        cv2.line(frame,(sx, sy),(ex, ey),(255,0,0),10) 

        box = np.int0(box)
        cv2.drawContours(frame,[box], 0, (255, 0, 255), 2)
        
        # show the rotated start point
        # (rotX, rotY) = rotatePoints(lineStart,Y,X,Y,angle)
        # cv2.circle(frame,(rotX,rotY), 50, (0,255,255), -1)

        cv2.imshow("Frame", frame)

def findTopRectSide(box):
    """Returns the longest of two sides"""
    # return the two side numbers which are longest
    longestSide = [0,0]
    # keep track of the longest side
    longest = 0

    # check which of two sides is longer
    for i in range(2):
    
        # find the longest side
        length = lengthBetween2Points(box[i], box[i+1])    
        if  length >longest:
            longest = length
            longestSide = [i, i+1]

    return longestSide

def lengthBetween2Points(loc1, loc2):
    return cv2.norm(loc1,loc2)

def rotatePoints(Ox,Oy, Px,Py, angle):
    """ Rotate the x,y points around a central point by a specific angle """
    # convert angle into radians
    angle = 90
    radians = angle*(math.pi/180)
    print("This is the angle: {} , this is the radians: {}".format(angle, radians))

    # first translate the start points by the nagative of the pivotpoints
    Mx = Ox- Px
    My = Ox -Py

    # then rotate the points
    v = (int(Mx*math.cos(radians) - My*math.sin(radians)), int(Mx*math.sin(radians) + My*math.cos(radians)))
    # print("These are the rotated points: {}, These are the originals: x {}, y {}".format(v,Ox, Oy ))
    return v

def findContours(mask):
    # find contours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    # initialise (x,y) ball centre
    targetCenter = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour
        contour = max(cnts, key=cv2.contourArea)
        # ((x, y), radius) = cv2.minEnclosingCircle(contour)
        ((x,y), (width, height), angle) = cv2.minAreaRect(contour)


        # # calculate the contour centre
        # M = cv2.moments(contour)
        # cX = int(M["m10"] / M["m00"])
        # cY = int(M["m01"] / M["m00"])
        # targetCenter = (cX, cY)
        
        # (h, w) = mask.shape[:2]
        # Dist = distToCentre(w, cX)
        # print("these are the contours x: {}, y:{}, distance from the centreline: {}".format(cX, cY, Dist))

def distToCentre(ImgW, cX):
    # calculate the horizontal distance between the target and central vertical line
    Dist = int(abs((ImgW/2)- cX))
    return Dist

## designed to work out how long something takes to acomplish
def timeAction(processTime, cmd, name):
    
    # return process time dict if at start
    if cmd == "start":
        processTime['start'] = time.time()
        return processTime

    elif cmd == "end":
        sTime = processTime['start']
        eTime = time.time()
        totalTime = eTime-sTime

        # print("The process {} took this amount of time: {}".format(name, totalTime))