###
## this uses the base Omxplayer without python wrapper
###

import os
from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)


mainMenu = ["1_drums.mp3", "2_hello.mp3", "3_lineSearch.mp3", "4_red.mp3", "5_yellow.mp3"]

count =1
while True:
    # if (GPIO.input(23) == False):
    #     os.system('mpg123 -q binary-language-moisture-evaporators.mp3 &')

    # if (GPIO.input(24) == False):
    #     os.system('mpg123 -q power-converters.mp3 &')

    # if(done):  
    # if (GPIO.input(5)== False):
    print("This is mainmenu 1: {}".format(mainMenu[count]))

    try:

        target = "omxplayer " + mainMenu[count]
        os.system(target)
        # os.system('mpg123 -C hello.mp3')

        print("sleeping")

        count+=1

        if count ==(len(mainMenu)):
            count =0
        print("iteration: ")
    except KeyboardInterrupt:
        print("Exiting...")
        break

