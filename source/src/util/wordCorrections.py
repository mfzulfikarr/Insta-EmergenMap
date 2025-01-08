from util.utils import TextUtils
from collections import defaultdict, Counter
import dill
import os
from util.wfdistCalc import wagnerFischer
curr_dir = os.path.dirname(os.path.dirname(__file__))
utils = TextUtils()
def wordFreq_calc(sentences):
    wordCounts = Counter()
    for sentence in sentences:
        words = sentence.split()
        wordCounts.update(words)
    return wordCounts
def findCandidate(missWords, rootCorpus, wordFrequencies, threshold=4):
    corrected_words = {}
    for misspelled in missWords:
        close_matches = []
        for root_word in rootCorpus:
            distance = wagnerFischer(misspelled, root_word)
            if distance <= threshold:
                frequency = wordFrequencies.get(root_word, 0)
                close_matches.append((root_word, distance, frequency))
        # Sort by distance first, then by frequency (higher frequency comes first)
        close_matches.sort(key=lambda x: (x[1], -x[2]))
        # Keep only the words and limit to top 20
        corrected_words[misspelled] = [word for word, _, _ in close_matches[:15]]
    return corrected_words
# Calculate word frequencies
wordFrequencies = wordFreq_calc(utils.ngramCorpus)
def loadBigram(file_path):
    with open(file_path, 'rb') as file:
        return dill.load(file)
# Load the model
loaded_model = loadBigram(os.path.join(curr_dir, "util/models/bigramModel.dill"))
# Choosing the correct words contextually with N-Grams
def bigramReplace(tokens, correctWords, modelBigrams):
    corrected_tokens = []
    for i, token in enumerate(tokens):
        if token in correctWords:
            candidates = correctWords[token]
            if len(tokens) == 1:
                # If token or text only have one word then get first candidate
                best_fit = candidates[0]
            else:
                # Score each candidate based on bigram probabilities
                scores = []
                for candidate in candidates:
                    score = 0
                    if  i> 0:
                        prev_token = tokens[i - 1]
                        score += modelBigrams[prev_token][candidate]
                    if i < len(tokens) - 1:
                        next_token = tokens[i + 1]
                        score += modelBigrams[candidate][next_token]
                    scores.append((candidate, score))
                # Select the candidate with the highest score
                if scores:
                    best_fit = max(scores, key=lambda x: x[1])[0]
                else:
                    best_fit = token
            corrected_tokens.append(best_fit)
        else:
            corrected_tokens.append(token)
    return corrected_tokens