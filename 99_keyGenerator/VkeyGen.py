## This script creates and outputs Visual keys appending the unique combination 
## and correponding message to a json file: 

# Tasks
# - takes an input argument
# - generates a visual key
# - saves the key to file
# - makes sure the 

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import os
import json


###
## ARGPARSE
###

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description = 'intake key Name')

ap.add_argument("-m", "--message",help="encoded message")
ap.add_argument("-p", "--print",help="print all images to localDir")

# parse the arguments
args = vars(ap.parse_args())

print("This is the args: {}\n\n\n".format(args))

###
## Static Vals
###

## Dimensions
totHeight = 453 # mm
totWidth = 528 # mm

# calculate the segment dimensions
segmentH = int(totHeight/3)
segmentW = int(totWidth/2)


# current saved dict location
loc = "../savedDict.json"

NUMCOLORS = 6
# list of target colors RGB =>(BGR)
colors = {
    # "1":(255,34,0), # red
    # "2":(0,68,255), # blue
    # "3":(255,213,0), # yellow
    # "4":(43,255,0), # green
    # "5":(237,62,103), # purple

    "1":(0,68,255), # red
    "2":(255,0,0), # blue
    "3":(0,255,255), # yellow
    "4":(0,255,0), # green
    "5": (255,255,0), #turquoise
    "6":(255,0,239), # purple

}

DISPLAY = True


####################################### Functions ############################################



###
# 1. Check the input arguments
###

def checkArgs(args):
    inputVals = {}
    message = args.get("message", False)

    if message == False :
        print("No input message found. Exiting")
        exit()

    inputVals["message"] = message 

    return inputVals

###
## 2. import the remote dictionary
###
def importCurVals(location):
    """Imports the current list of combinations and messages"""
    # check that dict file exists
    if os.path.isfile(location):
        try: 
            with open(location, 'r') as fp:
                remoteDict = json.load(fp)
            print("Remote Dict opened and imported:\n{}".format(remoteDict))
            return remoteDict
    
        except:
            print("This is not json loadable")
    else:
        print("Currently no remote Dict, will generate on exit")
 
    return

###
## 3. Create a novel VCode for input vals
###
# validate the input

    # check for duplicates of the message in the remoteDictionary
def findMessage(RDict, message):
    for n in RDict:
        if message in RDict[n]:
            return RDict[n]
    return False

def findName(remoteDict, name):
    try:
        if name in remoteDict:
        # if(remoteDict[name]):
            print("The input Name: {} is already in the remoteDict please change it and repeat\n\n".format(name))
            return False
    except:
        return True
        # print("The name is not a duplicate\n")


    # check that the message don't exist in the RemoteDict
def checkForDups(remoteDict, message):
    # check for duplicate value in remoteDict if duplicate then show error message
    if findMessage(remoteDict, message) != False:
        print("The input Message: {} is already in the remoteDict please change it and repeat\n\n".format(message))
        return


def numCreator(a,b,c,d):
    """convert the random numbers into a 4 digit int"""
    output =0

    output += a*1000 
    output += b*100
    output += c*10
    output += d

    output = int(output)
    return output

def genCode(remoteDict, NUMCOLORS):
    """Find a novel key combination"""
    count = 0
    for tl in range(1, NUMCOLORS):
        for tr in range(1, NUMCOLORS):
            for br in range(1, NUMCOLORS):
                for bl in range(1, NUMCOLORS):
                    num = numCreator(tl, tr, br, bl)
                    # print("GENCODE: This is the remoteDict Number: {}".format(num))                

                    if(findName(remoteDict, num)==True):
                        print("Number found: {}".format(num))
                        return num
                    # keep track of the number of iterations
                    count+=1

    return False

###
## 4. Create new VCode image
###

# Create rectangles for the VCode keys

    # Add the Colored Keys
def addKeys(colors, num, frame):
    """Create and populate image with keys"""    

    # frame, (topLeft(x,y)), (bottomRight(x,y))
    cv2.rectangle(frame,(0,0),(264,segmentH),(colors[num[0]]),-1)
    cv2.rectangle(frame,(0,segmentH),(264,int(segmentH*2)),(colors[num[1]]),-1)
    cv2.rectangle(frame,(264,0),(totWidth,segmentH),(colors[num[2]]),-1)
    cv2.rectangle(frame,(264,segmentH),(totWidth,int(segmentH*2)),(colors[num[3]]),-1)

    # bottom segment
    cv2.rectangle(frame,(0,int(segmentH*2)),(totWidth,int(segmentH*3)),(colors["6"]),-1)

    return frame

def addText(text, frame, height, width):

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,text,(50, height+95), font, 2,(255,255,255),4,cv2.LINE_AA)
    return frame


# Add text below VCode
# Display novel VCode

###
## 5. Save novel VCode image
###

###
## 6. Save local VCode definitions to file
###
def writeToFile(location, localDict):
    remoteDict = open(location, 'w')
    remoteDict.write(localDict)

    print("This is the remoteDict:\n{}".format(remoteDict))


def clearDir(location):
    filelist = [ f for f in os.listdir("keys/") if f.endswith(".png") ]

    for f in filelist:
        imgLoc = location + f
        print("Removing files: {}".format(imgLoc))
        os.remove(imgLoc)


##################################################### Main #################################################


## 1. Check the input arguments
inputVals = checkArgs(args)

## 2. import the remote dictionary
RDict = {}
RDict = importCurVals(loc)
# RDict = {"bestName":1234}

if(args.get("print", False)):
    print("Printing time!!!\n\n\n")
    
    # clear img directory
    clearDir("keys/")

    # recreate all images
    for q in RDict:
        print("This is RDict i: {}".format(q))
        # Create a black/blank image
        frame = np.zeros((totHeight+100, totWidth,3), np.uint8)    

        # Add the Colored Keys+Anchor
        frame = addKeys(colors, q, frame)
        # Add text below VCode
        frame = addText(q, frame, totHeight, totWidth)
        
        ## Save novel VCode image
        fileName = 'keys/' + q + '.png'
        cv2.imwrite(fileName, frame)


elif(args.get("message", False)):
    print("Lets create some keys\n\n\n")

    ## 3. Create a novel VCode for input vals
    # validate the input
        # check that the name doesn't exist in the RemoteDict
        # check that the value doesn't also exist in the RemoteDict
    print("This is the inputVals: {}".format(inputVals))
    checkForDups(RDict, inputVals["message"])


    # Find a novel combination
    name = genCode(RDict, NUMCOLORS)
    name = "1111"

    ## 4. Create new VCode image
    # Create rectangles for the VCode keys

    # Create a black/blank image
    frame = np.zeros((totHeight+100, totWidth,3), np.uint8)    

    # Add the Colored Keys+Anchor
    frame = addKeys(colors, "1234", frame)
    # Add text below VCode
    frame = addText("1234", frame, totHeight, totWidth)

    # Display novel VCode
    if(DISPLAY):
        cv2.imshow("frame", frame)
        cv2.waitKey(0)

    ## 5. Save novel VCode image
    fileName = 'keys/' + name + '.png'
    cv2.imwrite(fileName, frame)

    ## 6. Save novel VCode to file
    with open(loc, 'w') as fp:
        json.dump(RDict, fp, sort_keys=True, indent=4)




