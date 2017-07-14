### requires these 'alsa-utils mpg123' be installed with sudo apt-get 
#####

# -= terminal control keys =-
# [s] or [ ]	interrupt/restart playback (i.e. 'pause')
# [f]	next track
# [d]	previous track
# [b]	back to beginning of track
# [p]	pause while looping current sound chunk
# [.]	forward
# [,]	rewind
# [:]	fast forward
# [;]	fast rewind
# [>]	fine forward
# [<]	fine rewind
# [shift and +]	volume up
# [-]	volume down
# [r]	RVA switch
# [v]	verbose switch
# [l]	list current playlist, indicating current track there
# [t]	display tag info (again)
# [m]	print MPEG header info (again)
# [h]	this help
# [q]	quit
# [c] or [C]	pitch up (small step, big step)
# [x] or [X]	pitch down (small step, big step)
# [w]	reset pitch to zero

import os
from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)

# GPIO.setup(24, GPIO.IN)
# GPIO.setup(25, GPIO.IN)

while True:
    # if (GPIO.input(23) == False):
    #     os.system('mpg123 -q binary-language-moisture-evaporators.mp3 &')

    # if (GPIO.input(24) == False):
    #     os.system('mpg123 -q power-converters.mp3 &')

    # if(done):  
    if (GPIO.input(5)== False):
        print("Inside..")
        os.system('mpg123 -C hello.mp3')
        print("sleeping")
        sleep(1)
    sleep(1)
    print("iteration: ")