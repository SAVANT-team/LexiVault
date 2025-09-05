# library of functions for calculating metrics
from collections import Counter
from .morphemo import Morphemo, saveFile, splitCorpus, loadWordsInData
import re
import gdown
import datetime

def wordfreq(text):
    # use regex to split text into words (alphanumeric sequences)
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

def morphemo():
    # TODO this is the sample; actually implement
    # I will provide you with an example corpus

    file_ids = [
        "1FJL8RBJintQ0_FZQjvN2gAaWpD8MzB5H",
        "1xZ7MZE5CQ-PeJx2LlVRI34ALicaKMFPw",
        "1PqPEFoqKlcVnpkIPNYXNP-4JrhhVpjc9"
    ]

    for fid in file_ids:
        url = f"https://drive.google.com/uc?id={fid}"
        gdown.download(url, output=None, quiet=False)

    corpusPath = 'bribri-conllu-20240314-corpus.txt'
    goldstandardPath = 'bribri-conllu-goldstandard-corpus.txt'
    untrainedCorpus = "bribri-unmarked-corpus.txt"
    numberRun = "01"

    # Split into train and test
    splitCorpus(corpusPath, goldstandardPath, numberRun)
    # Instantiate Morphemo
    morphemo_model = Morphemo(UNSEEN_BIAS=2, lookahead=2)

    goldTraining = "train-gold-"+numberRun+".txt"
    hypTest = "test-corpus-"+numberRun+".txt"

    # Train
    x = datetime.datetime.now()
    print(x)
    morphemo_model.train(untrainedCorpus, goldTraining)
    x = datetime.datetime.now()
    print(x)

    # Analyze the words in a text file
    testWords = loadWordsInData(hypTest)
    analyzedWords = []
    for t in testWords:
        morphemo_results_raw = morphemo_model.ortho_morpher(t)
        analyzedWords.append(morphemo_results_raw)
    saveFile("test-corpus-"+numberRun+"-morphemo.txt", '\n'.join(analyzedWords))

    # Analyze a single word
    word = "bua'ë"
    morphemo_res = morphemo_model.ortho_morpher(word)
    print(word + " --> " + morphemo_res)