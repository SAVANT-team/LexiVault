'''
INPUT: .txt / .csv / .xlsx corpus uploaded by user
OUTPUT: .csv file in /db
'''
import csv
from func_lib.func_lib import wordfreq
from pathlib import Path

class InputProcessor:
    text = ''
    filepath = ''

    def __init__(self, language, run_wordfreq, run_morph_decomp):
        self.language = language
        self.run_wordfreq = run_wordfreq
        self.run_morph_decomp = run_morph_decomp

        # path for saving output file
        self.savepath = Path('db_new') / f'{self.language}.csv'

    def process_txt(self, filepath):
        # read text from file
        with open(filepath, 'r', encoding='utf-8') as f:
            self.text = f.read()

        # run desired functions
        if self.run_wordfreq:
            wordfreq_counts = wordfreq(self.text)
            # write to csv file
            with open(self.savepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['word', 'wordfreq'])
                for word, count in wordfreq_counts.items():
                    writer.writerow([word, count])
        
        if self.run_morph_decomp:
            print("Running morphological decomposition...")
