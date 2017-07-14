import RPi.GPIO as GPIO
import time
import imutils
import cv2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)


for i in range(5):
    print("LED on")
    GPIO.output(16,GPIO.HIGH)
    time.sleep(1)
    print("LED off")
    GPIO.output(16,GPIO.LOW)
    time.sleep(1)

print("Cleaning up GPIO pins and closing.")
GPIO.cleanup()