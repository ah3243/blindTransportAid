
class motorControl:
    """a basic class to control the vibration motor"""
    # set class variables
    motorVal = 0 
    distance = 0
    maxPWM = 50

    def __init__(self, maxDist):
        ## set instance variables

        # set the maximum Distance depending on image size
        self.maxDist = maxDist 

    def setMotorVal(self, val):
        """Set the motor value"""
        self.motorVal = val
        # print("This is the new motor value: {}".format(self.motorVal))
        pass

    def invertVal(self, val):
        """Invert a value in relation to a specific range"""
        RMin = 0
        RMax = self.maxPWM

        # find the range
        rang = RMax- RMin

        # invert the value and adjust to fit within range min -> return
        return RMin + (rang - val)

    def mapToRange(self,val):
        """Map a value to a new range, and invert the value"""
        # convert the orgin range into 0-1 range
        scaledORange = float(val)/float(self.maxDist)

        scaledDRange = int(scaledORange * self.maxPWM)
        invScaledVal = self.invertVal(scaledDRange)

        return invScaledVal

    def calcMotorVal(self, dist):
        """Calculate the PWM value"""
        # if the value is larger than the boundary print an error and put to max pwm
        if dist>self.maxDist:
            # print("No target within specified distance {}".format(dist))
            return 0

        return  self.mapToRange(dist)
        
    def setDistance(self, val):
        """Main Set distance function"""
        self.distance = val
        if(self.distance == -1 | self.distance > self.maxDist):
            self.setMotorVal(0)

        pwmVal = self.calcMotorVal(val)
        self.setMotorVal(pwmVal)
    
