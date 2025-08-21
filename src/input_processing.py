"""
function to take in input (corpus uploaded by user)
"""
import csv
from collections import Counter
from pathlib import Path
from .func_lib import wordfreq

class InputProcessor:
    def __init__(self, filepath, run_wordfreq=True, run_morph_decomp=True):
        self.filepath = filepath
        self.run_wordfreq = run_wordfreq
        self.run_morph_decomp = run_morph_decomp
        self.text = ""

        # saving to temp_db/out
        self.save_path = Path("temp_db/out") / f"{self.filepath.stem}.csv"
            
    def process(self):
        if self.filepath.suffix == ".txt":
            self.process_txt();
        # TODO non-txt files
        else:
            print("TODO")
    
    def process_txt(self):
        # read text from file
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.text = f.read()
        
        # run desired functions
        if self.run_wordfreq: 
            wordfreq_counts = wordfreq(self.text)
            with open(self.save_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["word", "wordfreq"])
                for word, count in wordfreq_counts.items():
                    writer.writerow([word, count])