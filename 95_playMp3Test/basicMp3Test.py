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

mainMenu = ["01_yellow.mp3", "02_red.mp3", "03_orange.mp3", "04_blue.mp3"]

count =1
while True:
 
    print("current track: {}".format(mainMenu[count]))

    target = "mpg123 -C " + mainMenu[count]
    os.system(target)

    print("sleeping")
    sleep(1)

    count+=1

    if count ==(len(mainMenu)):
        count =0
    print("iteration: ")
