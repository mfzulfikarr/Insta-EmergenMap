import pandas as pd
import os
from collections import defaultdict, Counter
from util.utils import TextUtils
from util.keyList import keyValue
from util.wordCorrections import bigramReplace, loaded_model, findCandidate, wordFrequencies
curr_dir = os.path.dirname(__file__)
utils = TextUtils()
dfRaw = pd.read_csv(os.path.join(curr_dir, '../Datasets/mergedData.csv'))
df = dfRaw.copy()
# Preprocess the data so it can be easily filtered
df['textClean'] = df['content'].apply(utils.casefolding)
df['textClean'] = df['textClean'].apply(utils.removedigitCensor)
for pattern, replacement in utils.abbreviations.items():
    df['textClean'] = df['textClean'].str.replace(pattern, replacement, regex=True)
df['textClean'] = df['textClean'].apply(utils.removeLinks)
df['textClean'] = df['textClean'].apply(utils.removeTags)
df['textClean'] = df['textClean'].apply(utils.removeSymbols)
df['textClean'] = df['textClean'].apply(utils.removeDigit)
df['textClean'] = df['textClean'].apply(utils.removeCredit)
df['textClean'] = df['textClean'].apply(utils.removeSlogan)
df['textClean'] = df['textClean'].apply(utils.removeSinglechar)
df['textClean'] = df['textClean'].apply(utils.removeRomannum)
df['textClean'] = df['textClean'].apply(utils.removeSpaces)
df['textToken'] = df['textClean'].apply(utils.tokenization)
df['textToken'] = df['textToken'].apply(utils.stopwordIndo_token)
df['textToken'] = df['textToken'].apply(utils.normalizeText)
def contains_keywords(tokens, keywords):
    return any(keyword in ' '.join(tokens) for keyword in keywords)
# Filter the data first so less data and less computing resource for stemming
dfFiltered = df[df['textToken'].apply(lambda tokens: contains_keywords(tokens, keyValue))]
dfFiltered.reset_index(drop=True, inplace=True)
# Now stemming so it's easier and more accurate for misspelled word correction
dfStem = dfFiltered.copy()
dfStem['textToken'] = dfStem['textToken'].apply(utils.stemmingIndo_token)
dfStem['textToken'] = dfStem['textToken'].apply(utils.moreStemming)
dfStem['textToken'] = dfStem['textToken'].apply(utils.removeAbbrev)
# Starts the filtering
uniqueWords = set([word for tokens in dfStem['textToken'] for word in tokens])
# Filter out words that are not misspelled but not in the corpus
uniqueWords_fil = [word for word in uniqueWords if word not in utils.notmisspelled and word not in utils.singkatanList and word not in utils.engrootCorpus]
# Iterate through unique words in your corpus and compare with root words corpus
missWords = []
for word in uniqueWords_fil:
    if word not in utils.rootCorpus and word: # Ensure word is not empty
        missWords.append(word)
correctWords = findCandidate(missWords, utils.rootCorpus, wordFrequencies)
# Re-stem and removing stopword again because the word that are corrected might actually not in a form of root words or might be a stopword
dfStem['textToken'] = dfStem['textToken'].apply(lambda tokens: bigramReplace(tokens, correctWords, loaded_model))
dfStem['textToken'] = dfStem['textToken'].apply(utils.stemmingIndo_token)
dfStem['textToken'] = dfStem['textToken'].apply(utils.stopwordIndo_token)
dfStem.to_excel(os.path.join(curr_dir, '../Datasets/cleanData.xlsx'), index=False)
dfStem.to_csv(os.path.join(curr_dir, '../Datasets/cleanData.csv'), index=False)