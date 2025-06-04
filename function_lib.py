# library of functions for calculating metrics
from collections import Counter
import re

def wordfreq(text):
    # use regex to split text into words (alphanumeric sequences)
    words = re.findall(r'\w+', text.lower())
    return Counter(words)