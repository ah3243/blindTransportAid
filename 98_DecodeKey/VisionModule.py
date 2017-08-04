import time
import cv2
import numpy as np
import math

# values for pink (VL, VH, HL, HH, SL, SH)
OPEN = [0, 255, 0, 180, 0, 255]
#target colors
Purple = [36, 189, 172, 179, 26, 251] # the distinctive purple color
Purple_Black = [19, 214, 161, 179, 160, 255] # for ~1ft black background dark

Cur = Purple_Black
## assign variables
hul = Cur[2]
huh = Cur[3]
sal = Cur[4]
sah = Cur[5]
val = Cur[0]
vah = Cur[1]


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
    message = findPurpleDems(mask, frame)
    
    return message


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
        # print("This is the box var: {}".format(box))
        # print("This is the y distance: {}".format(box[0][1]))

        ## Find and decode the keys ##

        # calculate the average anchor height(related to key y positions)
        avgHeight = avgAnchorHeight(box)

        # calculate position of each of four keys
        keyPos = calcKeyPositions(avgHeight, box)

        # get the Hue values of pixel at each key location(save in single 4 digit int)
        hueVals = getKeyVals(keyPos, frame)

        # retrive string corresponding to key arrangement
        message = decodeKey(hueVals)


        # display the keyPos positions
        for i in keyPos :
            # print("This is the hsv of pixel 50,50: {}".format(frame[spotPointx][spotPointy]))
            cv2.circle(frame,(i[0],i[1]), 10, (0,255,255), -1) # yellow

        cv2.circle(frame,(keyPos[1][0],keyPos[1][1]), 15, (0,0,0), -1)
        # print("pixel Loc: {}   pixelValue: {}".format(keyPos[1],frame[keyPos[1][1],keyPos[1][0]]))

        cv2.imshow("Frame", frame)

        return message

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
    
    # make sure all values are within the image size
    rightKey = betweenRange(rightKey, 600)
    leftKey = betweenRange(leftKey, 600)
    topKey = betweenRange(topKey, 600)
    btmKey = betweenRange(btmKey, 600)

    print("This is the average left col: {}, average right: {}".format(leftKey, rightKey))
    print("This is the average top row: {}, average bottom row: {}".format(topKey, btmKey))

    return [(leftKey, topKey), (rightKey, topKey), (leftKey, btmKey), (rightKey, btmKey)]

def betweenRange(input, topRange):
    """Make sure values dont exceed the image size"""
    if input >=topRange:
        return topRange-1
    else: 
        return input

def getKeyVals(KeyPos, frame):
    """Return the Hue values from the 4 segments"""    

    hueVals = 0
    counter =1000 # create 4 digit number to hold results

    for i in KeyPos:
        tmpVal = recogniseHue(frame[i[1]][i[0]][0])
        hueVals += (counter*tmpVal)
        counter = counter/10 # save from largest to smallest digit(1000->1)
 
    return hueVals

def recogniseHue(inHue):
    red = (0, 9)
    yellow = (16, 33)
    green = (39, 89) 
    blue = (96, 129) 
    purple = (165, 179) # (anchor)

    if(inHue>red[0] and inHue < red[1]):
        print("It's red")
        return 1
    elif(inHue>yellow[0] and inHue < yellow[1]):
        print("It's yellow")
        return 2
    elif(inHue>green[0] and inHue < green[1]):
        print("It's green")
        return 3
    elif(inHue>blue[0] and inHue < blue[1]):
        print("it's blue")
        return 4
    elif(inHue>purple[0] and inHue < purple[1]):
        print("It's purple")
        return 5
    else:
        print("Error: color not recongised")
        return False

def decodeKey(inputVal):
    """Find and decode key value"""

    ## Dict for pattern to string matching
    # - segments measured anti clockwise from top left
    # - a number between 1 and 5 denotes the color hue
    dictVals = {
        1111: "all blue",
        1221: "testValue",
        2222: "all yellow",
        3333: "all green",
        4444: "all red",
        1234:"Hello multicultural world!!",
        4231: "you finally got it!!!"
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