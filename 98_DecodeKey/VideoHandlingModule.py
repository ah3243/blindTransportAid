import time
import datetime
import cv2
import imutils

def finish(vs, fps, SAVE, writer):
    # do a bit of cleanup
    print("[INFO] cleaning up")
    fps.stop() # calculate fps values
    vs.stop()

    if SAVE:
        writer.release()

    # display fps values
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    time.sleep(2) # wait for 2 seconds for the video to save    

def getVidName():
    Tme = datetime.datetime
    rootName = "TestVid"
    Tme = Tme.now()
    curTime = "_" + str(Tme.hour) + "-" + str(Tme.minute)
    print("hours: {}, minutes: {}".format(Tme.now().hour, Tme.now().minute))
    extension = ".avi"
    vidName = rootName + curTime + extension

    print("This is the time now: {}\n This is the vidName: {}".format(curTime, vidName))
    return vidName

def createVideoWriter(vs, imgW):
    # initialize the FourCC, video writer, dimensions of the frame, and
    # zeros array
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = None
    (h, w) = (None, None)
    zeros = None
    defaultFps = 25

    vidName = getVidName()

    frame = vs.read()
    frame=cv2.flip(frame,-1)
    frame = imutils.resize(frame, width=imgW)        
    (h, w) = frame.shape[:2]

    writer = cv2.VideoWriter(vidName, fourcc, defaultFps,
        (w, h), True)

    return writer