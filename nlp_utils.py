# coding: utf-8
from __future__ import unicode_literals
import re
from math import isfinite
from word2number import w2n
from typing import Union
from nltk.tokenize import word_tokenize
# from nltk.tokenize.stanford import StanfordTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from .contraction import CONTRACTION_MAP
from .regex import remove_punctuation
wordnet_lemmatizer = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer('english')


def tokenize(text: str, with_contraction: bool=False,
              with_punc: bool=True) -> str:
    """
    with_punc: (optional) whether to include punctuation as separate tokens.
    with_contraction: (optional) whether to replace contraction words into
                multigrams before tokenizing.
    Returns: list of word tokens.
    """
    if with_contraction:
        text = expand_contractions(text)
    tokens = word_tokenize(text)
    if with_punc:
        return tokens
    else:
        return [word if word.startswith("'") else remove_punctuation(word)
                for word in tokens if remove_punctuation(word)]


def lemmatize(text: str, method: str='wordnet') -> str:
    """Apply lemmatizer/Stemmer to the words in text.
    It can be operated with either WordNetLemmatizer or Snowball Stemmer
    Returns: text with lemmatized tokens.
    """
    tokens = tokenize(text)
    if method == 'wordnet':
        cleaned_tokens = [wordnet_lemmatizer.lemmatize(token) for token in tokens]
    elif method == 'snowball':
        cleaned_tokens = [snowball_stemmer.stem(token) for token in tokens]:
    else:
        raise Exception("Error - lemmatizer method not supported")

    return ' '.join(cleaned_tokens)


def convert_text_to_number(text: str) -> Union[int, float]:
    """Transform text format of number into digit (int or float).
    word_to_num: able to convert common digit string to digit,
                e.g. `forty` to 40, but cannot handle `40` as 40.
    Returns: digit value of numbers in text."""
    if text:
        try:
            num = w2n.word_to_num(text)
            return num
        except (ValueError, IndexError):
            pass
    return convert_text_to_float(text)


def convert_text_to_float(text: str) -> float:
    "Transform text format of float value to float."
    try:
        if isfinite(float(text)):
            return float(text)
    except (ValueError, IndexError):
        return None



def convert_text_to_bool(text) -> bool:
    "Transform bool type string to bool value"
    if text.lower() == "yes":
        return True
    elif text.lower() == "no":
        return False
    return numpy.nan


def remove_nonascii_chars(text: str) -> str:
    """Return string with NonAscii characters removed."""
    letters = []
    for l in text:
        if(ord(l) < 128):
            letters.append(i)
        else:
            letters.append(" ")
    return "".join(letters).strip()


def expand_contractions(text: str, contraction_mapping=CONTRACTION_MAP) -> str:
    """Expand constraction expression in sentence to multigrams, to better
    catch the meaning before tokenziation.
    e.g. `hasn't` to `has not` to realize the negation signal."""
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text
