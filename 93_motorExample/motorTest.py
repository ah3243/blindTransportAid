import RPi.GPIO as GPIO
import cv2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor1 = 13
pwmFreq = 200


# GPIO.cleanup()

GPIO.setup(motor1, GPIO.OUT)
# set PWM pins and frequency
PWM_M1 = GPIO.PWM(motor1, pwmFreq)
PWM_M1.start(0)

while(True):
    for x in range(100):
        PWM_M1.start(x)
        k =  cv2.waitKey(10)

    for x in range(100):
        PWM_M1.start(100-x)
        k =  cv2.waitKey(10)


while(True):
    print("turning motor ON")
    GPIO.output(motor1, GPIO.HIGH)

    k =  cv2.waitKey(5000)
    if k == ord('q'):
        print("exiting")
        GPIO.output(motor1, GPIO.LOW)
        GPIO.cleanup()
        exit()
    else:
        print("next")
    print("turning motor OFF")
    GPIO.output(motor1, GPIO.LOW)

    k =  cv2.waitKey(1000)
    if k == ord('q'):
        print("exiting")
        GPIO.output(motor1, GPIO.LOW)
        GPIO.cleanup()
        exit()
    else:
        print("next")

GPIO.cleanup()