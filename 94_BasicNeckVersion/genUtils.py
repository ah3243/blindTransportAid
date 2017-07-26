###
##  This is a brief library for working with a vibration motor array
##  transforming distances into the various PWM motor outputs    
###

# for exponential transform
from math import pow
 
# main function to handle the different types of feedback
def getFeedbackVal(distance, leftMin, leftMax, rightMin, rightMax, feedbackType):
    # return PWM value
    value = 0
    powOfVal = 10

    if feedbackType == 1:
        print("normal feedback chosen")

        # get linear mapping of value to between 0-100
        value = translate(distance, leftMin, leftMax, rightMin, rightMax)

    elif feedbackType == 2:

        # map value to between 0-70
        value = int(translate(distance, leftMin, leftMax, rightMin-30, rightMax))

        # if target is within 10% range of the centre then increase the vibration by 30
        if((distance/leftMax<=0.1) and feedbackType==2):
            value+=30
        
    elif feedbackType == 3:
        fractionDist = (distance-leftMin)/(leftMax-leftMin)
        value = int(pow(fractionDist, powOfVal))
        # make sure starting range is for exponential values
        leftMax = int(pow(leftMax, powOfVal))
        print("\nexponential feedback chosen. This is the dist: {}, value: {}, leftMax: {}, fractionalVal: {}".format(distance, value, leftMax, fractionDist))

        # map exponential values to between 0-100
        value = int(translate(value, leftMax, leftMin, rightMin, rightMax))
        print("This is value: {}".format(value))

    elif feedbackType == 4:
        print("melody feedback chosen")

    else:
        print("ERROR: the getFeedbackVal() function has received an incorrect 'feedbackType' variable value. Exiting")
        exit(1)

    return value


def translate(val, oldMax, oldMin, newMax, newMin):

    oldSpan = (oldMax - oldMin)  
    newSpan = (newMax - newMin)  

    newValue = (((val - oldMin) * newSpan) / oldSpan) + newMin

    newValue = (((val - oldMin)/oldSpan)*newSpan) + newMin
    # Figure out how 'wide' each range is

    # print("This is the oldMin: {}, oldMax: {}, newMin: {}, newMax: {}, and decimalVal: {}".format(oldMin, oldMax, newMin, newMax, val/oldSpan))

    # leftSpan = leftP - leftM
    # rightSpan = rightP - rightM

    # # Convert the left range into a 0-1 range (float)
    # valueScaled = float(val - leftM) / float(leftSpan)

    # # Convert the 0-1 range into a value in the right range.
    # newVal = rightM + (valueScaled * rightSpan)
    
    # print("value: {}, Left span: {}, right span: {}, newValue: {}".format(val, oldSpan, newSpan, newValue))

    return newValue

