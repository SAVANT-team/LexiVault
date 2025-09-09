'''
INPUT: .txt / .csv / .xlsx corpus uploaded by user
OUTPUT: .csv file in /db
'''
import csv
from func_lib.func_lib import wordfreq


class InputProcessor:
    text = ""
    filepath = ""

    def __init__(self, run_wordfreq):
        self.run_wordfreq = run_wordfreq

    def process_txt(self, filepath):
        # read text from file
        with open(filepath, 'r', encoding='utf-8') as f:
            self.text = f.read()

        # run desired functions
        if self.run_wordfreq:
            print("running wordfreq")
            wordfreq_counts = wordfreq(self.text)
            print(wordfreq_counts)
