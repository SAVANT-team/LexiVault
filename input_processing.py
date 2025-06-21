"""
function to take in input (corpus uploaded by user)
"""
from function_lib import *

class InputProcessor:
    def __init__(self, text, wantedAttributes=["wordfreq"]):
        # automatically assume we want word frequency generated
        self.text = text
        self.wantedAttributes = wantedAttributes
    
    def process(self):
        # calculate specified-for attributes

        # word frequency
        if "wordfreq" in self.wantedAttributes:
            print(wordfreq(self.text))
            # TODO: currently this only prints; i want a PD dataframe
        
        # morphological decomposition