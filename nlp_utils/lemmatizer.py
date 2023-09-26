# -*- coding: utf-8 -*-
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

wordnet_lemmatizer = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer("english")


def lemmatize(word: str, pos=None, method: str = "wordnet") -> str:
    """Apply lemmatizer/Stemmer to the words in text.
    It can be operated with either WordNetLemmatizer or Snowball Stemmer
    """
    if method == "wordnet":
        cleaned_word = wordnet_lemmatizer.lemmatize(word, pos) if pos else wordnet_lemmatizer.lemmatize(word)
    elif method == "snowball":
        cleaned_word = snowball_stemmer.stem(word)
    else:
        raise Exception("Error - lemmatizer method not supported")
    return cleaned_word
