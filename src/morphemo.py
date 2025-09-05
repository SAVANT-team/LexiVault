import numpy as np
import datetime
import random

class Morphemo:
   """
   Morphemo class is a class that predicts the likelihood of morpheme boundaries in a word given the environment.
   """
   # tokens
   start_token : str = "<s>"
   end_token : str = "</s>"
   morph_token : str = "+"
   # text probabilities
   text_forward_prob : np.ndarray
   text_backward_prob : np.ndarray
   text_forward_index : dict[str, int]
   text_backward_index : dict[str, int]
   # morph probabilities
   morph_forward_prob : np.ndarray
   morph_backward_prob : np.ndarray
   morph_forward_index : dict[str, int]
   morph_backward_index : dict[str, int]
   # morph frequency data
   morph_freq_data : np.ndarray
   # lookahead
   lookahead : int = 2
   # unseen bias
   UNSEEN_BIAS : float = 2

   def __init__(self, start_token : str = "<s>", end_token : str = "</s>", morph_token : str = "+", lookahead : int = 2, UNSEEN_BIAS : float = 2):
      """
      Constructor for Morphemo class.

      Parameters:
      @param start_token: token to be inserted at the beginning of the word
      @param end_token: token to be inserted at the end of the word
      @param morph_token: token to be inserted as morpheme boundary
      @param lookahead: number of characters to look ahead in x-gram training
      @param UNSEEN_BIAS: bias to be applied to unseen data
      """
      self.UNSEEN_BIAS = UNSEEN_BIAS
      self.lookahead = lookahead

      # set start, end, morphology tokens
      self.start_token = start_token
      self.end_token = end_token
      self.morph_token = morph_token

   def train(self, untagged_file : str, morph_file : str) -> None:
      """
      Trains the model with untagged text and morpheme data.

      Parameters:
      @param untagged_file: file containing untagged text
      @param morph_file: file containing morpheme data
      """

      print(untagged_file)
      print(morph_file)

      with open(untagged_file, 'r', encoding="utf8") as f:
         untagged_text : str = f.read().split()

      with open(morph_file, 'r', encoding="utf8") as f:
         morph_text : str = f.read().split()

      # load text probabilities (same indices because it is a square matrix)
      self.text_forward_prob, self.text_forward_index, temp = self.probability_loader(untagged_text, lookahead=self.lookahead)
      self.text_backward_prob, temp, self.text_backward_index = self.probability_loader(untagged_text, reversed=True, lookahead=self.lookahead)

      # load morpheme probabilities
      self.morph_forward_prob, self.morph_forward_index, temp = self.probability_loader(morph_text, filter_token="+", lookahead=1)
      self.morph_backward_prob, temp, self.morph_backward_index = self.probability_loader(morph_text, filter_token="+", reversed=True, lookahead=self.lookahead)

      # load morpheme frequency data
      self.morph_freq_data = self.morphemes_percentage(morph_text)

   def probability_loader(self, text = list[str], filter_token : str = None, lookahead : int = 1, reversed : bool = False) -> np.ndarray:
      """
      Loads text files and calculates the probability of each x-gram following another character.

      Parameters:
      @param text_files: list of text files to be loaded
      @param pre_token: token to be used as a filter for the previous character
      @param post_token: token to be used as a filter for the x-gram
      @param lookahead: number of characters to look ahead (x-gram size)

      Returns:
      @return probabilities: np array of probabilities
      """
      words = [self.word_cutter(word, self.start_token, self.end_token) for word in text]

      # enumerate all characters and assign an index to them
      set_chars : set[str] = set()
      set_grams : set[tuple[str]] = set()
      chars_grams : dict[str, dict[tuple[str], int]] = {}

      # load the characters and grams into dictionaries (one-pass)
      for word in words:
         for i in range(0, len(word)):
            set_chars.add(word[i])
            if i < len(word)-lookahead:
               # account for short morpheme
               if reversed and self.morph_token in word[i+1:i+lookahead+1]:
                  gram_list = word[i+1:i+lookahead+2]
                  gram_list.remove(self.morph_token)
                  gram : tuple = tuple(gram_list)
               else:
                  gram : tuple = tuple(word[i+1:i+lookahead+1])

               set_grams.add(gram)

               # new gram
               if word[i] not in chars_grams:
                  chars_grams[word[i]] = {}
               if gram not in chars_grams[word[i]]:
                  chars_grams[word[i]][gram] = 0

               # increment gram count
               chars_grams[word[i]][gram] += 1

      char_to_index : dict[int, str]= {char : i for i, char in enumerate(sorted(set_chars))}
      gram_to_index : dict[int, tuple[str]] = {gram : i for i, gram in enumerate(sorted(set_grams))}

      # create np array of probabilities (row = previous char, column = next char)
      probabilities : np.ndarray = np.zeros((len(set_chars), len(set_grams)))

      # update the probabilities array
      for char in chars_grams:
         for gram in chars_grams[char]:
            count = chars_grams[char][gram]
            probabilities[char_to_index[char], gram_to_index[gram]] = count

      # transform the array if looking backwards
      if reversed:
         probabilities = np.transpose(probabilities)

      # normalize the probabilities
      for row in probabilities:
         np.log10(np.divide(row,np.sum(row)), out=row, where=np.sum(row))
      probabilities[probabilities==0] = self.UNSEEN_BIAS * np.min(probabilities[probabilities!=0])

      # filter the probabilities if a token is specified
      if filter_token is not None:
         probabilities = probabilities.take([char_to_index[filter_token]], axis=1, mode='clip')

      return probabilities, char_to_index, gram_to_index

   def morphemes_percentage(self, morphemes : list[str]) -> np.ndarray:
      """
      Calculates the frequency of morpheme counts given word lengths.

      Parameters:
      @param morphemes: list of morphemes

      Returns:
      @return morph_freq_data: np array of morpheme frequencies
      """
      morpheme_freq : list[tuple[int, int]] = []
      max_morphemes = 0
      max_wordlength = 0

      for word in morphemes:
         word_chars : list[str] = self.word_cutter(word, "<s>", "</s>")
         morph_count : int = word_chars.count("+")
         word_length : int = len(word_chars)

         # update max values for data array dimensions
         if word_length > max_wordlength:
            max_wordlength = word_length
         if morph_count > max_morphemes:
            max_morphemes = morph_count

         morpheme_freq.append((word_length, morph_count))

      # create data array
      morph_freq_data = np.zeros((max_wordlength + 1, max_morphemes + 1))
      for word_length, morph_count in morpheme_freq:
         morph_freq_data[word_length, morph_count] += 1

      # reduce the effect of length bias
      np.sqrt(morph_freq_data, out=morph_freq_data, where=morph_freq_data!=0)

      for row in morph_freq_data:
         if np.sum(row) != 0:
            np.log10(row / np.sum(row), out=row, where=row!=0)

      morph_freq_data[morph_freq_data==0] = self.UNSEEN_BIAS * np.min(morph_freq_data[morph_freq_data!=0])

      return morph_freq_data

   def predict_word(self, raw_word : str) -> list[str]:
      """
      Predicts the likelihood of morpheme boundaries in a word.

      Parameters:
      @param raw_word: string representing a word

      Returns:
      @return morph_indexes: list of indices where morpheme boundaries are likely to occur
      """

      word : list[str] = self.word_cutter(raw_word, self.start_token, self.end_token)

      # calculate base probabilities
      base_prob : list[float] = [0] * (len(word) - self.lookahead)
      for i in range(0, len(word) - self.lookahead):
         base_prob[i] = self.point_score(word[i], tuple(word[i+1:i+self.lookahead+1]))

      # calculate morpheme probabilities
      morph_prob : list[tuple[int, float]] = [0] * (len(word) - self.lookahead)
      for i in range(0, len(word) - self.lookahead):
         morph_prob[i] = (self.morph_score(word[i], tuple(word[i+1:i+self.lookahead+1])), i)

      morph_prob.sort(key=lambda x: x[0], reverse=True)

      # determine likelihood of morphemes that are present
      n_morphemes : int = 0
      morph_indexes : list[int] = []
      for morph, i in morph_prob:
         #+ self.get_morph_count_freq(len(word), n_morphemes)
         if base_prob[i]  < morph: #+ self.get_morph_count_freq(len(word), n_morphemes+1):
            n_morphemes += 1
            morph_indexes.append(i+1)

      return morph_indexes

   def point_score(self, before : str, after : tuple[str]) -> float:
      """
      Calculates the score of a location in the word given the grams before and after the point.

      Parameters:
      @param before: character before the point
      @param after: character after the point

      Returns:
      @return score: score of the point
      """
      forward : float
      backward : float

      # calculate forward looking probability
      if before in self.text_forward_index and after in self.text_backward_index:
         forward = self.text_forward_prob[self.text_forward_index[before], self.text_backward_index[after]]
      else:
         forward = self.text_forward_prob.min() * self.UNSEEN_BIAS
      # calculate backward looking probability
      if after in self.text_backward_index and before in self.text_forward_index:
         backward = self.text_backward_prob[self.text_backward_index[after], self.text_forward_index[before]]
      else:
         backward = self.text_backward_prob.min() * self.UNSEEN_BIAS

      return forward + backward

   def morph_score(self, before : str, after : str) -> float:
      """
      Calculates the score of a morpheme boundry given the grams before and after the boundary.

      Parameters:
      @param before: character before the morpheme boundary
      @param after: character after the morpheme boundary

      Returns:
      @return score: score of the morpheme boundary
      """
      forward : float
      backward : float
      # calculate forward looking probability
      if before in self.morph_forward_index:
         forward = self.morph_forward_prob[self.morph_forward_index[before]][0]
      else:
         forward = self.morph_forward_prob.min() * self.UNSEEN_BIAS

      # calculate backward looking probability
      if after in self.morph_backward_index:
         backward = self.morph_backward_prob[self.morph_backward_index[after]][0]
      else:
         backward = self.morph_backward_prob.min() * self.UNSEEN_BIAS

      return forward + backward

   def get_morph_count_freq(self, word_length : int, morph_count : int) -> float:
      '''
      Returns the frequency of a morpheme count given a word length.

      Parameters:
      @param word_length: length of the word
      @param morph_count: number of morphemes in the word

      Returns:
      @return frequency: frequency of the morpheme count given the word length (min val if not found)
      '''

      if word_length >= self.morph_freq_data.shape[0] or morph_count >= self.morph_freq_data.shape[1]:
         return self.UNSEEN_BIAS * np.min(self.morph_freq_data)
      return self.morph_freq_data[word_length, morph_count]

   @staticmethod
   def word_cutter(word : str, start_token : str, end_token : str) -> list[str]:
      """
      Cuts a word into a list of characters with start and end tokens.

      Parameters:
      @param word: string representing a word
      @param start_token: token to be inserted at the beginning of the word
      @param end_token: token to be inserted at the end of the word

      Returns:
      @return word: list of characters with start and end tokens
      """
      return [start_token] + [*word.lower()] + [end_token]

   @staticmethod
   def word_morpher(word : list[str] | str, morph_token : str, morph_locations : list[int]) -> list[str]:
      """
      Inserts morpheme tokens into a word at specified locations.

      Parameters:
      @param word: list of characters representing a word
      @param morph_token: token to be inserted as morpheme boundary
      @param morph_locations: list of indices where the morpheme token should be inserted

      Returns:
      @return word: list of characters with morpheme tokens inserted
      """
      insert_count : int = 0

      for i in sorted(morph_locations):
         word.insert(i + insert_count, morph_token)
         insert_count += 1

      return word

   def ortho_morpher(self, word : str) -> str:
      """
      Inserts morpheme tokens into a word based on orthographic rules.

      Parameters:
      @param word: string representing a word

      Returns:
      @return word: string with morpheme tokens inserted
      """
      word_list : list[str] = self.word_cutter(word, self.start_token, self.end_token)
      morph_locations : list[int] = self.predict_word(word)
      word_list_final : list[str] = self.word_morpher(word_list, self.morph_token, morph_locations)

      return "".join(word_list_final[1:len(word_list_final)-1])

def saveFile(filename, text, typeOfSave="w"):
  f = open(filename, typeOfSave)
  f.write(text)
  f.close()

def splitCorpus(corpus_path, goldstandard_path, splitNumber):
    # Step 1: Read both files and create a combined list of lines
    with open(corpus_path, 'r') as corpus_file, open(goldstandard_path, 'r') as goldstandard_file:
        corpus_lines = corpus_file.readlines()
        goldstandard_lines = goldstandard_file.readlines()

    # Check if both files have the same number of lines
    if len(corpus_lines) != len(goldstandard_lines):
        raise ValueError("Both files must have the same number of lines.")

    # Create the combined list
    lines = [corpus_lines[i].strip() + ' — ' + goldstandard_lines[i].strip() for i in range(len(corpus_lines))]

    # Step 2: Shuffle the lines randomly
    random.shuffle(lines)

    # Step 3: Split into training and testing sets
    split_index = int(0.8 * len(lines))  # Calculate 80% index
    trainingTemp = lines[:split_index]  # First 80%
    testingTemp = lines[split_index:]  # Last 20%

    trainingCorpus = []
    trainingGold = []

    for i in range(0, len(trainingTemp)):
      temp = trainingTemp[i].split(" — ")
      trainingCorpus.append(temp[0])
      trainingGold.append(temp[1])

    testCorpus = []
    testGold = []

    for i in range(0, len(testingTemp)):
      temp = testingTemp[i].split(" — ")
      testCorpus.append(temp[0])
      testGold.append(temp[1])

    oTrainingCorpus = '\n'.join(trainingCorpus)
    oTrainingGold = '\n'.join(trainingGold)

    oTestCorpus = '\n'.join(testCorpus)
    oTestGold = '\n'.join(testGold)

    saveFile("train-corpus-"+splitNumber+".txt", oTrainingCorpus)
    saveFile("train-gold-"+splitNumber+".txt", oTrainingGold)

    saveFile("test-corpus-"+splitNumber+".txt", oTestCorpus)
    saveFile("test-gold-"+splitNumber+".txt", oTestGold)

    print("Training Data:")
    print(len(trainingTemp))
    print("\nTesting Data:")
    print(len(testingTemp))
#=======================================================
# This loads the words from a text file into a list
# that contains those words.
#=======================================================

def loadWordsInData(filename):

  retArray = []

  f = open(filename, "r")
  lines = f.readlines()

  for l in lines:
    l = l.strip()
    l = l.split(" ")
    for w in l:
      retArray.append(w)

  return(retArray)