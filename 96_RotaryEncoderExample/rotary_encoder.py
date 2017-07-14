from RPi import GPIO
from time import sleep

# clk = 17
# dt = 18

clk = 6
dt = 12
sw = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(clk)

try:

        while True:
                # pushBtn = GPIO.input(sw)
                # if pushBtn !=1:
                #         print("button pressed..")
                        
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)

                if clkState != clkLastState:
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        print counter
                clkLastState = clkState
                sleep(0.01)
finally:
        GPIO.cleanup()