## this is a class which intakes text and is able to transform it into synthesised speach

import os
def speakCurrent(inputSpeech):
    text = 'flite -t "' + inputSpeech + '"'
    print("This is the text: {}".format(text)) 
    os.system(text)