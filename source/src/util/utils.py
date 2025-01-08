import re
import json
import os
import nltk #import library nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import word_tokenize #import word_tokenize for tokenizing text into words
from nltk.tokenize import sent_tokenize #import sent_tokenize for tokenizing paragraph into sentences
from nltk.stem.porter import PorterStemmer #import Porter Stemmer Algorithm
from nltk.stem import WordNetLemmatizer #import WordNet lemmatizer
from nltk.corpus import stopwords #import stopwords (English)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory #import Indonesian Stemmer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory #import Indonesian Stopword remover
from Sastrawi.StopWordRemover.StopWordRemover import StopWordRemover
from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
curr_dir = os.path.dirname(os.path.dirname(__file__))

class TextUtils:
    def __init__(self):
        self.rootCorpus = self.read_txt(os.path.join(curr_dir, '../corpuses/katadasarSastrawi.txt'))
        self.notmisspelled = self.read_txt(os.path.join(curr_dir,'../corpuses/notmisspCustomMerged2.txt'))
        self.singkatanList = self.read_txt(os.path.join(curr_dir,'../corpuses/singkatanIndolower.txt'))
        self.engrootCorpus = self.read_txt(os.path.join(curr_dir,'../corpuses/englishwordsDwyl_final.txt'))
        self.iklanWords = self.read_txt(os.path.join(curr_dir,'../corpuses/kataiklanCustom.txt'))
        self.ngramCorpus = list(self.read_txt(os.path.join(curr_dir,'../corpuses/ngramDataset1m_all.txt')))
        with open(os.path.join(curr_dir,'../corpuses/abbrevFix.json'), 'r', encoding='utf-8') as jsonAbbrev:
            self.abbreviations = json.load(jsonAbbrev)
        with open(os.path.join(curr_dir,'../corpuses/digitConv.json'), 'r', encoding='utf-8') as jsonDigits:
            self.digit_to_char = json.load(jsonDigits)

        #StopwordsRemover Initiate
        self.addStopwords = ['dll', 'dst', 'dsb', 'lho', 'loh', "lah", "nih", "noh", "nah"]
        self.swfactory = StopWordRemoverFactory()
        self.defaultStopwords = self.swfactory.get_stop_words()
        # customStopwords = list(filter(lambda word: word not in ['tidak', 'di'], defaultStopwords))
        self.customStopwords = self.defaultStopwords + self.addStopwords
        self.newDict = ArrayDictionary(self.customStopwords)
        self.stopword = StopWordRemover(self.newDict)

        #Stemmer Initiate
        self.stemfactory = StemmerFactory()
        self.stemmer = self.stemfactory.create_stemmer()
        self.prefixNg = re.compile(r'^ng(.*)')
        self.prefixDi = re.compile(r'^di(.*)')
        self.prefixPeny = re.compile(r'^peny(.*)')
        self.prefixPer = re.compile(r'^per(.*)')
        self.suffixNg = re.compile(r'(in|nya)$')
        self.suffixAn = re.compile(r'an$')
        self.suffixNya = re.compile(r'nya$')

    def read_txt(self, filePath):
        with open(filePath, 'r', encoding='utf-8') as file:
            return set(line.strip() for line in file)

    #sentence tokenization
    def sentence_tokenization(self, text):
        return sent_tokenize(text)
    # word tokenization
    def tokenization(self, text):
        return word_tokenize(text)

    #stopword Indonesian
    def stopwordIndo(self, word):
        return self.stopword.remove(word)
    def stopwordIndo_token(self, tokens):
        return [word for word in tokens if self.stopwordIndo(word) != '']

    #Stemming Indonesian
    def stemmingIndo(self, text):
        return self.stemmer.stem(text)
    def stemmingIndo_token(self, tokens):
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return stemmed_tokens

    # Remove affixes and check root corpus
    def moreStemming(self, tokens):
        def removeAffix(word):
            if word in self.rootCorpus:
                return word
            if self.prefixNg.match(word):
                word = self.prefixNg.sub(r'k\1', word)
                word = self.suffixNg.sub('', word)
            elif self.prefixDi.match(word) and self.suffixNg.search(word):
                word = self.suffixNg.sub('', word)
            elif self.prefixPeny.match(word):
                word = self.prefixPeny.sub(r's\1', word)
                word = self.suffixAn.sub('', word)
            elif self.prefixPer.match(word):
                word = self.suffixAn.sub('', word)
            else:
                word = self.suffixNya.sub('', word)
            return word
        makeStem = [removeAffix(word) for word in tokens]
        return self.stemmingIndo_token(makeStem)

    # Remove digit
    def removeDigit(self, text):
        new_string =  re.sub(r"[0-9]", "", text)
        return new_string
    # Remove digit in between string
    def removedigitCensor(self, text):
        def replaceMatch(match):
            word = match.group()
            for digit, char in self.digit_to_char.items():
                word = word.replace(digit, char)
            return word
        pattern = re.compile(r'\b(?!(?:\d+\w+|\w+\d+)\b)\w*[a-zA-Z]\d\w*\b|\b(?!(?:\d+\w+|\w+\d+)\b)\w*\d[a-zA-Z]\w*\b')
        return pattern.sub(replaceMatch, text)
    # Remove tags
    def removeTags(self, text):
        tagString = re.sub(r'#\w+', '', text) #remove hashtag (#)
        tagString = re.sub(r'@\s?[\w.]+', '', tagString) #remove mention (@)
        return tagString
    #remove symbols
    def removeSymbols(self, text):
        clnString = re.sub(r'\n+', ' ', text) #remove newlines (\n)
        clnString = re.sub(r"[$%#@*']", "", clnString)
        clnString = re.sub(r"[^ a-zA-Z0-9=-]", " ", clnString) #remove symbols(.,<>\/,etc.)
        clnString = re.sub(r'-', ' ', clnString)
        return clnString
    # Remove spaces
    def removeSpaces(self, text):
        removeSpc = re.sub(r"\s+", " ", text).strip()
        return removeSpc
    # Remove credit
    def removeCredit(self, text):
        credString = re.sub(r'\bcredit\s*by\b', '', text)
        credString = re.sub(r'\bvia\s*\b', '', credString)
        credString = re.sub(r'\bsource\s*\b', '', credString)
        credString = re.sub(r'\binfo\s*\b$', '', credString)
        credString = re.sub(r'\bcr\b.+$', '', credString)
        credString = re.sub(r'\bby\b.+$', '', credString)
        return credString

    # casefolding
    def casefolding(self, text):
        currString = text.lower()
        return currString

    #remove links or websites
    def removeLinks(self, text):
        # no_links = re.sub(r'https?://\S+|www\.\S+', '', text)
        noLinks = re.sub(r'(http|https)://\S+|www\.\S+|bit\.\S+|linktr\.\S+|desty\.\S+', '', text)
        noLinks = re.sub(r"\b\w+\.(com|org|net|gov|ly)\b", '', noLinks)
        noLinks = re.sub(r"\b\w+\s+(com|org|net|gov|ly)\b", '', noLinks)
        noLinks = re.sub(r"\b\w+\.?(com|org|net|gov|ly)\b", '', noLinks)
        # noLinks = re.sub(r"\b\w+|\b[a-z]+\.[a-z]{1,2}/\S+", '', noLinks)
        return noLinks
    # Remove slogan
    def removeSlogan(self, text):
        noSlogan = re.sub(r'untuk share info.+$', '', text)
        return noSlogan
    def removeAbbrev(self, tokens):
        noAbbrev = [word for word in tokens if len(word) != 3 or word in self.singkatanList or word in self.rootCorpus]
        return noAbbrev
    # Remove single character word
    def removeSinglechar(self, text):
        return re.sub(r'\b\w\b', '', text)
    # Remove roman numerals
    def removeRomannum(self, text):
        romanPattern = r'\b(?:M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\b' # Pattern for matching Roman numerals (case-insensitive)
        return re.sub(romanPattern, '', text, flags=re.IGNORECASE)

    def normalizeText(self, tokens):
        normalTokens = []
        for token in tokens:
            # Check if the token is in the English word corpus
            if token.lower() not in self.engrootCorpus and token.lower() not in self.singkatanList:
                # Pattern for replacing sequences of the same character at the end of the token with just one of the same character (yaa to ya, excluding english word like free)
                fixedToken = re.sub(r'(.)\1+$', r'\1', token)
                normalTokens.append(fixedToken)
            else:
                normalTokens.append(token)
        return normalTokens