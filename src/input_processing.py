"""
function to take in input (corpus uploaded by user)
"""
from .func_lib import wordfreq

class InputProcessor:
    def __init__(self, filepath, wordfreq=True):
        self.filepath = filepath
        self.wordfreq = wordfreq
    
    def process(self):
        print(self.filepath)