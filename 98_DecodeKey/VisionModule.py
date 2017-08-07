import time
import cv2
import numpy as np
import math


# values for pink (VL, VH, HL, HH, SL, SH)
OPEN = [0, 255, 0, 180, 0, 255]
#target colors
Purple = [36, 189, 172, 179, 26, 251] # the distinctive purple color
Purple_Black = [19, 214, 161, 179, 160, 255] # for ~1ft black background dark
Purple_Black_Day = [19, 255, 161, 179, 160, 255] # for ~1ft black background dark

Cur = Purple_Black_Day
## assign variables
hul = Cur[2]
huh = Cur[3]
sal = Cur[4]
sah = Cur[5]
val = Cur[0]
vah = Cur[1]


def findColor(frame, DISPLAY, MOTOR, motor, cmdDict):
    """initial function, create HSV range+mask and passes to 'findPurpleDems'"""
    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])

    # it is common to apply a blur to the frame
    frame=cv2.GaussianBlur(frame,(5,5),0)

    # #create a mask for that range
    mask = cv2.inRange(frame,HSVLOW, HSVHIGH)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    if DISPLAY:
        # show the frames
        cv2.imshow("Frame2", mask)
        key = cv2.waitKey(1) & 0xFF # give it time to process            
    message = findPurpleDems(mask, frame, DISPLAY, MOTOR, motor, cmdDict)
    
    
    # unless false is returned return message
    if message == False:
        # print("False returned, REturning false: {}\n\n\n".format(message))
        return False
    else: 
        return message


# def angleDirection(rect, box, point):
#     """Work out which way to rotate the key sample points"""

#     if box[0][1] > box[1][1]:
#         angle = abs(rect[2])
#         print("Returning positive angle: {}".format(angle))
#         return angle
#     elif box[0][1] < box[1][1]:
#         angle = rect[2]
#         print("Returning negative angle: {}".format(angle))
#         return angle
#     else: 
#         return False


# def rotatePoint(origin, point, radians):
#     """Rotate a point counterclockwise around a given origin by angle in radians"""

#     ox, oy = origin
#     px, py = point

#     qx = int(ox + math.cos(radians) * (px - ox) - math.sin(radians) * (py - oy))
#     qy = int(oy + math.sin(radians) * (px - ox) + math.cos(radians) * (py - oy))
#     return qx, qy

def findPurpleDems(mask, frame, DISPLAY, MOTOR, motor, cmdDict):
    """main holding function, finds contour, creates best fit box"""
    # find contours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    # only continue if there is at least one contour
    if len(cnts) > 0:
        # find the largest contour
        contour = max(cnts, key=cv2.contourArea)

        # find the smallest bounding rectangle, it's size position and orientation

        #  rect == ((x,y), (width, height), angle)
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        # print("This is what's inside the rect(): {}, width: {} height: {}".format(rect[2], rect[1][0], rect[1][1]))

        # The centre point of the rectangle
        centX = int(rect[0][0])
        centY = int(rect[0][1])            

        # rotAngle = angleDirection(rect, box, (centX, centY))

        # if  rotAngle != False:
        #     rotPoint = rotatePoint((centX, centY), (centX, centY+40), rotAngle)
        #     cv2.line(frame, (centX, centY), rotPoint, (0,255,0), 10)

        # else:
        #     print("\n\n\n\n\n Is False\n\n" )

        # font = cv2.FONT_HERSHEY_SIMPLEX

        # cv2.putText(frame,"0",(box[0][0], box[0][1]), font, 2,(255,255,255),4,cv2.LINE_AA)
        # cv2.putText(frame,"1",(box[1][0], box[1][1]), font, 2,(255,255,255),4,cv2.LINE_AA)
        # cv2.putText(frame,"2",(box[2][0], box[2][1]), font, 2,(255,255,255),4,cv2.LINE_AA)
        # cv2.putText(frame,"3",(box[3][0], box[3][1]), font, 2,(255,255,255),4,cv2.LINE_AA)
        # cv2.line(frame, (lineXL, centY), (lineXR, centY), (0,255,255), 4)

        lineXL = int(centX-50)
        lineXR = int(centX+50)



        # get the longest top side of the rectangle
        (sta,fin) = findLongRectSide(box)

        # convert box to np array???
        box = np.int0(box)
    
        if(DISPLAY):
            cv2.drawContours(frame,[box], 0, (255, 0, 255), 2)

    
        ## Find and decode the keys ##

        # calculate the average anchor height(related to key y positions)
        avgHeight = avgAnchorHeight(box)

        # get the anchors bounding box width and height side lengths, rtn false if not correct ratio(only partial anchor detected)
        lineLengths = isFullAnchor(avgHeight, box)
        if not lineLengths:
            # print("Returning False")
            return False

        # calculate position of each of four keys
        keyPos = calcKeyPositions(avgHeight, box)

        # get the Hue values of pixel at each key location(save in single 4 digit int)
        hueVals = getKeyVals(keyPos, frame)
        hueVals = str(int(hueVals))
        # retrive string corresponding to key arrangement
        message = decodeKey(hueVals, motor, cmdDict, MOTOR)

        ## set the vibration motor to the correct amount based on horizontal distance to target centre
        xVal = int(rect[0][0])
        yVal = int(rect[0][1])

        # cv2.circle(frame,(xVal,yVal), 10, (100,0,100), -1)
        dist = distToCentre(frame.shape[1], xVal)

        # set the distance
        if MOTOR:
            motor.setDistance(dist)

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

def getXorYVals(box, sortList, xORy):
    """returns a list of x or y values, sorted or unsorted"""
    yList = []
    
    # create a list of all xORy values (flag determines which one)
    for i in range(4):
        yList.append(box[i][xORy])
   
    # sort the list
    if sortList:
        yList.sort()

    return yList

def isFullAnchor(avgDems, box):
    """Check the whole anchor has been identified(by the known ratio of average height to width, rtn true is so otherwise rtn false"""
    lineLengths = []

    # acceptable range of ratios between width and height of anchor(height*ratio == width) 
    ratioRange = [1.5, 4.9] # ideal ratio is 3.5

    # calc length of two sides(identical to other two sides)
    for a in range(2):
        b = a+1

        lineLengths.append(getLineLength(box[a], box[b]))

    # sort the list to seperate the width and length measurements
    lineLengths.sort()
    print("\nThis is the lineLengths: {}".format(lineLengths))

    cBtm = lineLengths[0] *ratioRange[0]
    cTop = lineLengths[0] *ratioRange[1]

    if lineLengths[1]>cBtm and lineLengths[1]<cTop:
        return lineLengths
    else:
        print("not within range..")
        return False

def getLineLength(pos1, pos2):
    """calculate the straight line distance between two x,y points"""
    dist = math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)  
    return dist

def distToCentre(ImgW, cX):
    # calculate the horizontal distance between the target and central vertical line
    Dist = int(abs((ImgW/2)- cX))
    return Dist

def calcKeyPositions(avgHeight, box):
    """Work out where the colored key positions should be in relation to the purple locator"""
    # Vertical Ratio of points:
    # (1==1==1) both keys and anchor have an equal vertical size
    
    ## Calculate the y positions
    # find the anchor top row values(smallest two y values)
    yList = getXorYVals(box, 1, 1)
    avgTopRow = (yList[0]+yList[1])/2

    # calculate the y positions (based on the ratio of 1-1-1 for y values from top to bottom)
    # the conversion values are therefore:
    BtmRowMultiplier = .4 # go down half to get in the middle of the key (.2 instead of .5 for fine tuning)
    btmKey = avgTopRow - (avgHeight*BtmRowMultiplier)
    btmKey = int(btmKey)

    TopRowMultiplier = 1.4 # go down one then half to get in the middle of the key (.2 instead of .5 for fine tuning)
    topKey = avgTopRow - (avgHeight*TopRowMultiplier)
    topKey = int(topKey)

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
    
    return [(leftKey, topKey), (rightKey, topKey), (leftKey, btmKey), (rightKey, btmKey)]


def withinPicture(frame, i):
    """confirms that the sample position is within the frame to prevent errors"""
    ## Note that the frame dimenions are (y,x) while the i coordinates are (x,y)

    if (i[0] < 0 or i[1] < 0 ):
        # check that the sample position doesn't contain negative coordinates
        # print("ERROR: sample location below 0, i = {}".format(i))
        return False
    elif(i[0]<frame.shape[1] and i[1]<frame.shape[0]):
    # check that the sample position is within the frame
        return True

def getKeyVals(KeyPos, frame):
    """Return the Hue values from the 4 segments"""    

    hueVals = 0
    counter =1000 # create 4 digit number to hold results

    for i in KeyPos:
        # check that the sample location is within the image, else do not sample
        if withinPicture(frame, i):
            tmpVal = recogniseHue(frame[i[1]][i[0]][0])
            hueVals += (counter*tmpVal)
            counter = counter/10 # save from largest to smallest digit(1000->1)
        else:
            return False
    return hueVals

def recogniseHue(inHue):

    # red = (0, 9) # target = 4
    # yellow = (16, 33) # target = 25
    # green = (39, 89) # target = 55
    # blue = (96, 129) # target = 112
    # purple = (165, 179) # (anchor) # target = 173

    red = (0, 9) # target = 5
    yellow = (15, 40) # target = 30+-10
    green = (45, 75) # target = 60
    turquoise = (80, 109) # target = 90
    blue = (110, 140) # target = 120
    purple = (160, 172) # (anchor) # target = 150(much higher than thought)
 
    # print("This is the hue: {}".format(inHue))

    if(inHue>red[0] and inHue < red[1]):
        return 1
    elif(inHue>yellow[0] and inHue < yellow[1]):
        return 2
    elif(inHue>green[0] and inHue < green[1]):
        return 3
    elif(inHue>turquoise[0] and inHue < turquoise[1]):
        return 4
    elif(inHue>blue[0] and inHue < blue[1]):
        return 5
    elif(inHue>purple[0] and inHue < purple[1]):
        return 6
    else:
        # print("Error: color not recongised")
        return False

def decodeKey(inputVal, motor, cmdDict, MOTOR):
    """Find and decode key value"""

    ## Dict for pattern to string matching
    # - segments measured anti clockwise from top left
    # - a number between 1 and 5 denotes the color hue
    dictVals = {}
    dictVals = cmdDict.retnDict()

    # try and match the key values to saved keys
    try:
        message = dictVals.get(inputVal)  
        # print("This is the inputVal: {} and result: {} ".format(inputVal, message))
        return message

    except:
        # print("Exception: unable to find value in command dictionary")
        if MOTOR:
            motor.setDistance(0)
        return "No target"

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