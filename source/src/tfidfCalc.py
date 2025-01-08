import math
from collections import Counter
class SimpleTfidfVectorizer:
    def __init__(self):
        self.idf_ = {}
        self.vocab_ = []
        self.idf_default = 1.0
    def fit(self, corpus):
        N = len(corpus)
        df = Counter()
        for document in corpus:
            words = set(document.split())
            for word in words:
                df[word] += 1
        self.idf_ = {word: math.log(N / df[word]) for word in df}
        self.vocab_ = list(df.keys())
        return self
    def transform(self, corpus):
        tfidf_matrix = []
        for document in corpus:
            tfidf_vector = []
            tf = Counter(document.split())
            for word in self.vocab_:
                tfidf = (tf[word] / len(document.split())) * self.idf_.get(word, self.idf_default)
                tfidf_vector.append(tfidf)
            tfidf_matrix.append(tfidf_vector)
        return tfidf_matrix
    def fit_transform(self, corpus):
        self.fit(corpus)
        return self.transform(corpus)
