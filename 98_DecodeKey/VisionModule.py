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

    rightSide = True

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

        box = cv2.boxPoints(rect)
        # print("box: {}".format(box[0]))

        # get the longest top side of the rectangle
        (sta,fin) = findLongRectSide(box)

        # set value to positive if right side is being detected
        rightSide = isRightSide((sta,fin))


        # (sx, sy) = box[sta]
        # (ex, ey) = box[fin]
        # cv2.line(frame,(sx, sy),(ex, ey),(255,0,0),10) 
        # print("The line dimensions are sta: {} fin: {} ".format(sta, fin))

        box = np.int0(box)
        cv2.drawContours(frame,[box], 0, (255, 0, 255), 2)


        #### used as a test to check how to get a single pixels HSV value
        print("This is the box var: {}".format(box))
        print("This is the y distance: {}".format(box[0][1]))

        ## Find and decode the keys ##
        # calculate the average anchor height(related to key y positions)
        avgHeight = avgAnchorHeight(box)
        print("This is the avgHeight: {}".format(avgHeight))
        keyPos = calcKeyPositions(avgHeight, box)


        # cv2.line(frame,(0, keyPos[3][1]),(480, keyPos[3][1]),(255,0,0),10) 
        # cv2.line(frame,(keyPos[1][0], 0),(keyPos[1][0], 480),(255,0,255),5) 
        # cv2.line(frame,(keyPos[3][0], 0),(keyPos[3][0], 480),(255,0,0),5) 

        # display the keyPos positions
        for i in keyPos :
            # print("This is the hsv of pixel 50,50: {}".format(frame[spotPointx][spotPointy]))
            cv2.circle(frame,(i[0],i[1]), 10, (0,255,255), -1) # yellow

        # hueVals = getKeyVals(keyPos, frame)
        # message = decodeKey(hueVals)

        # show the rotated start point
        # cv2.circle(frame,(SX,SY), 10, (0,255,255), -1) # yellow
        # cv2.circle(frame,(SX1,SY1), 10, (255,255,255), -1) # white
        # cv2.circle(frame,(SX2,SY2), 10, (0,0,255), -1) # red
        # cv2.circle(frame,(SX3,SY3), 10, (0,255,0), -1) # green

        cv2.imshow("Frame", frame)

def findLongRectSide(box):
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

    findTopSide(box, longestSide)

    return longestSide

def lengthBetween2Points(loc1, loc2):
    return cv2.norm(loc1,loc2)

def findTopSide(box, longSide):
    """Find the top of two rect sides, (the one with the highest starting y value)"""
   
    # get the second npvalue(y value) from the first longSide value(start point)
    firstY = box[longSide[0]].item(1)

    Y2 = longSide[0]+2
    if Y2>3:
        print("Y2 over 3: start value: {}, corrected value: {}".format(Y2, Y2-2))
        Y2 = Y2-2
    secondY = box[Y2].item(1)

    if(firstY < secondY):
        pass
        # print("First y was smaller than second Y changing. This is the longSide output: {}".format(longSide))
        # Longside output was (1,2) and (1,2)
        # return secondY

def isRightSide(lineDems):
    """find out which side of the purple anchor is being detected, return true if it's the right side"""

    ## check wether the pixels on the right of the box are black, if so then return right == true
    if():
        return True
    else:
        return False

def distToCentre(ImgW, cX):
    # calculate the horizontal distance between the target and central vertical line
    Dist = int(abs((ImgW/2)- cX))
    return Dist

def getXorYVals(box, sortList, xORy):
    """returns a list of x or y values, sorted or unsorted"""
    yList = []
    
    # create a list of all y values
    for i in range(4):
        yList.append(box[i][xORy])
   
    # sort the list
    if sortList:
        yList.sort()

    return yList

def avgAnchorHeight(box):
    """Work out the average anchor y height"""
    ## find the two largest and two smallest y values
    yList = getXorYVals(box, 1, 1)
   
    ## combine the two largest and two smallest
    top = yList[0] + yList[1]
    bottom = yList[2] + yList[3]

    # subtract them from each other and divide by two to get avgHeight
    avgHeight = (bottom-top)/2

    return avgHeight

def calcKeyPositions(avgHeight, box):
    """Work out where the colored key positions should be in relation to the purple locator"""
    # example sample points

    ## Calculate the y positions
    # find the anchor top row values(smallest two y values)
    yList = getXorYVals(box, 1, 1)
    avgTopRow = (yList[0]+yList[1])/2

    # calculate the y positions (based on the ratio of 4.5-5-3.5 for y values from top to bottom)
    # the conversion values are therefore:
    TopRowMultiplier = (5+2)/3.5
    topKey = avgTopRow - (avgHeight*TopRowMultiplier)
    topKey = int(topKey)

    BtmRowMultiplier = (2)/3.5
    btmKey = avgTopRow - (avgHeight*BtmRowMultiplier)
    btmKey = int(btmKey)

    ## calculate the x positions
    # get a sorted list of x positions
    xList = getXorYVals(box, 1, 0)

    # find the average left and right columns
    avgLCol = (xList[0]+xList[1])/2
    avgRCol = (xList[2]+xList[3])/2

    # get the average length
    avgLength = avgRCol - avgLCol

    # get a left and right value 20% in from each side
    leftKey = int(abs(avgLCol+(avgLength*.20)))
    rightKey = int(abs(avgRCol-(avgLength*.20)))

    print("This is the average left col: {}, average right: {}".format(leftKey, rightKey))


    return [(leftKey, topKey), (rightKey, topKey), (leftKey, btmKey), (rightKey, btmKey)]
    # return leftPos

def getKeyVals(KeyPos, frame):
    """Return the Hue values from the 4 segments"""    

    pass

def decodeKey(inputVal):
    """Find and decode key value"""

    ## Dict for pattern to string matching
    # - segments measured anti clockwise from top left
    # - a number between 1 and 5 denotes the color hue
    dictVals = {
        1111: "all blue",
        2222: "all yellow",
        3333: "all green",
        4444: "all red",
        1234:"Hello multicultural world!!",
    }
    result = dictVals[inputVal]
    print(result)

    return dictVals[inputVal]



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