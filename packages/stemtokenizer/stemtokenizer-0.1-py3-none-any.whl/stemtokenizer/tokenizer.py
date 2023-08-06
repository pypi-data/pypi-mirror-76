from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


class stemtokenizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
    def __call__(self, doc):
        return [self.stemmer.stem(t) for t in word_tokenize(doc)]


