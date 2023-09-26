from __future__ import unicode_literals
from metaphone import doublemetaphone
from dataclasses import dataclass
import doctest
from nlp_utils.word_splitter import WordSplitter, WhiteSpaceSplitter


@dataclass
class Threshold:
    WEAK = 0.5
    NORMAL = 0.75
    STRONG = 0.9


def double_metaphone(value):
    """
    Returns the double metaphone encoding of the input value.
    
    >>> double_metaphone("hello")
    ('HL', '')
    
    >>> double_metaphone("")
    ('', '')

    >>> double_metaphone("New York City")
    ('NRKST', '')
    """

    return doublemetaphone(value)


def double_metaphone_compare(tuple1, tuple2, threshold):
    """
    Compares the double metaphone encodings of two input values and
    returns a boolean indicating if they match.
        (Primary Key = Secondary Key) = Normal Match
        (Alternate Key = Alternate Key) = Minimal Match
    
    >>> double_metaphone_compare("hello", "helo")
    False
    
    >>> double_metaphone_compare("potato", "potato")
    True
    
    >>> double_metaphone_compare("world", "")
    False
    
    >>> double_metaphone_compare("", "")
    True
    """
    if threshold == Threshold.WEAK:
        if tuple1[1] == tuple2[1]:
            return True
    elif threshold == Threshold.NORMAL:
        if tuple1[0] == tuple2[1] or tuple1[1] == tuple2[0]:
            return True
    else:
        if tuple1[0] == tuple2[0]:
            return True
    return False


def replace_non_alphanumeric(string):
    """
    Replaces all non-alphanumeric characters in the input string with spaces.

    >>> replace_non_alphanumeric("Hello world!")
    'Hello world'

    >>> replace_non_alphanumeric("Let's go for a walk.")
    'Let s go for a walk'
    """
    return ''.join([' ' if char not in string.ascii_letters + string.digits else char for char in string])


def similarity_token_count(text1: str, text2: str, word_splitter: WordSplitter=WhiteSpaceSplitter()) -> float:
    """
    Calculates the similarity score between two strings as the ratio of the number of common tokens to the total number of unique tokens.

    Args:
        text (str): The first input string.
        text (str): The second input string.

    Returns:
        float: The similarity score between 0 and 1.

    >>> similarity_token_count("Hello world!", "Hello")
    0.5

    >>> similarity_token_count("hello", "HELLO")
    1.0

    >>> similarity_token_count("apple", "")
    0.0

    >>> similarity_token_count("", "")
    0.0

    >>> similarity_token_count("Let's go for a walk.", "Let's go for a run!")
    0.8333333333333334
    """
    text1 = text1.lower()
    text2 = text2.lower()

    text1 = replace_non_alphanumeric(text1)
    text2 = replace_non_alphanumeric(text2)

    tokens1 = word_splitter.split_words(text1)
    tokens2 = word_splitter.split_words(text2)

    common_tokens = set(tokens1) & set(tokens2)
    similarity_score = len(common_tokens) / len(set(tokens1).union(set(tokens2)))

    return similarity_score


if __name__ == '__main__':
    doctest.testmod()