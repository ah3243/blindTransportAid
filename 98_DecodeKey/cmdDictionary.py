## Define keys:value dictionary
import os
import json

class cmdDictionary:

    codeBook = {}

    loc = "savedDict.json"

    def __init__(self):
        # import the current command dictionary
        self.codeBook = self.update()


    def update(self):
        """Imports the current list of combinations and messages"""
        # check that dict file exists
        if os.path.isfile(self.loc):
            try: 
                with open(self.loc, 'r') as fp:
                    remoteDict = json.load(fp)
                # print("Remote Dict opened and imported:\n{}".format(remoteDict))
                return remoteDict
        
            except:
                print("This is not json loadable")
        else:
            print("Currently no remote Dict, will generate on exit")
    
        return

    def retnDict(self):
        """Return current local dictionary"""
        return self.codeBook

## Create a dictionary class which has the stored values 
# and methods to convert indexes into the corresponding strings