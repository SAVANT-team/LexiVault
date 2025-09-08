# library of functions for calculating metrics
from collections import Counter
from .morphemo import Morphemo, saveFile as baseSaveFile, splitCorpus as baseSplitCorpus, loadWordsInData as baseLoadWordsInData
import re
import gdown
import os
import datetime

# for organization's sake make sure morphemo files don't get put in the root directory
OUTPUT_DIR = "./temp_db/morphemo"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# wrapper around morphemo.py's functions to enforce saving behavior
def saveFile(filename, text, typeOfSave="w"):
    if not os.path.isabs(filename):
        filename = os.path.join(OUTPUT_DIR, filename)
    baseSaveFile(filename, text, typeOfSave)

def splitCorpus(corpus_path, goldstandard_path, splitNumber):
    baseSplitCorpus(corpus_path, goldstandard_path, splitNumber)
    for fname in [
        f"train-corpus-{splitNumber}.txt",
        f"train-gold-{splitNumber}.txt",
        f"test-corpus-{splitNumber}.txt",
        f"test-gold-{splitNumber}.txt",
    ]:
        if os.path.exists(fname):
            os.replace(fname, os.path.join(OUTPUT_DIR, fname))

def loadWordsInData(filename):
    if not os.path.isabs(filename):
        filename = os.path.join(OUTPUT_DIR, filename)
    return baseLoadWordsInData(filename)

def wordfreq(text):
    """
    word frequency counter function
    """
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

def morphemo():
    """
    morphological decomposition function
    """
    file_ids = [
        "1FJL8RBJintQ0_FZQjvN2gAaWpD8MzB5H",
        "1xZ7MZE5CQ-PeJx2LlVRI34ALicaKMFPw",
        "1PqPEFoqKlcVnpkIPNYXNP-4JrhhVpjc9"
    ]

    download_dir = OUTPUT_DIR
    os.makedirs(download_dir, exist_ok=True)

    for fid in file_ids:
        url = f"https://drive.google.com/uc?id={fid}"
        gdown.download(url, output=os.path.join(download_dir, ""), quiet=False)

    corpusPath = os.path.join(download_dir, 'bribri-conllu-20240314-corpus.txt')
    goldstandardPath = os.path.join(download_dir, 'bribri-conllu-goldstandard-corpus.txt')
    untrainedCorpus = os.path.join(download_dir, "bribri-unmarked-corpus.txt")
    numberRun = "01"

    # test/train split
    splitCorpus(corpusPath, goldstandardPath, numberRun)

    morphemo_model = Morphemo(UNSEEN_BIAS=2, lookahead=2)

    goldTraining = f"train-gold-{numberRun}.txt"
    hypTest = f"test-corpus-{numberRun}.txt"

    x = datetime.datetime.now(); print(x)
    morphemo_model.train(untrainedCorpus, os.path.join(OUTPUT_DIR, goldTraining))
    x = datetime.datetime.now(); print(x)

    testWords = loadWordsInData(hypTest)
    analyzedWords = [morphemo_model.ortho_morpher(t) for t in testWords]

    saveFile(f"test-corpus-{numberRun}-morphemo.txt", '\n'.join(analyzedWords))

    word = "bua'ë"
    morphemo_res = morphemo_model.ortho_morpher(word)
    print(word + " --> " + morphemo_res)
