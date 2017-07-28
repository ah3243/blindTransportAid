###
## uses this python omxplayer wrapper (https://github.com/willprice/python-omxplayer-wrapper)
###
from omxplayer import OMXPlayer
from time import sleep


mainMenu = ["1_drums.mp3", "2_hello.mp3", "3_lineSearch.mp3", "4_red.mp3", "5_yellow.mp3"]

cnt = 0
while(True):
    # file_path_or_url = 'path/to/file.mp4'

    # This will start an `omxplayer` process, this might
    # fail the first time you run it, currently in the
    # process of fixing this though.
    player = OMXPlayer(mainMenu[cnt])

    # The player will initially be paused

    player.play()
    sleep(1)
    player.pause()

    # Kill the `omxplayer` process gracefully.
    player.quit()

    cnt+=1
    if cnt ==len(mainMenu):
        cnt=0
