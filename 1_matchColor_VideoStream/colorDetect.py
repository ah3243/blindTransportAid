# ###
# ## Finds and displays the target colors in video stream
# ###

# import numpy as np
# import cv2

# image = cv2.imread("testImage.png")

# # define the list of boundaries
# boundaries = [
# 	([17, 15, 100], [50, 56, 200]),
# 	([86, 31, 4], [220, 88, 50]),
# 	([25, 146, 190], [62, 174, 250]),
# 	([103, 86, 65], [145, 133, 128])
# ]

# # loop over boundaries and detect color
# for (lower, upper) in boundaries:
#     # create numpy arrays from the boundaries
#     lower = np.array(lower, dtype="uint8")
#     upper = np.array(upper, dtype="uint8")

#     # find the the colors within the specified boundaries and apply the mask
#     mask = cv2.inRange(image, lower, upper)
#     output = cv2.bitwise_and(image, image, mask= mask)

#     # show the masked image
#     cv2.imshow("images", np.hstack([image, output]))

#     # cv2.imshow("Wimage", mask)
#     cv2.waitKey(0)



# Python program for Detection of a 
# specific color(blue here) using OpenCV with Python
import cv2
import numpy as np 
import time
 
# Webcamera no 0 is used to capture the frames
cap = cv2.VideoCapture(0) 



cv2.namedWindow('res')

num_frames = 150
start = time.time()

curFrame = 0
# This drives the program into an infinite loop.
while(curFrame <150):  
    # print("Number: {}".format(curFrame))     
    # Captures the live stream frame-by-frame
    _, frame = cap.read() 

    # Converts images from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([110,50,50])
    upper_red = np.array([130,255,255])
 
    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured 
    # objects found in the frame.
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # The bitwise and of the frame and mask is done so 
    # that only the blue coloured objects are highlighted 
    # and stored in res


    res = cv2.bitwise_and(frame,frame, mask= mask)

    # cv2.imshow('res',res)
    # cv2.imshow('res',frame)    

    # # This displays the frame, mask 
    # # and res which we created in 3 separate windows.
    # k = cv2.waitKey(5)
    # if k == 27:
    #     break
    curFrame+=1

end = time.time()

totalTime = end - start
fps = num_frames/totalTime
print("This is the time taken: {} and the estimated number of frames {} ".format(totalTime, fps))

# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()
 
# release the captured frame
cap.release()