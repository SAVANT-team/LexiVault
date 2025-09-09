import re
from collections import Counter

def wordfreq(text):
    words = re.findall(r'\w+', text.lower())
    return Counter(words)