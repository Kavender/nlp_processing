# coding: utf-8
from spacy.tokens import Token, Span, Doc


def is_alphanum(token: Token, valid_punctuation_marks='-') -> bool:
    """Check whether token contains only alpha-numeric characters and valid punctuation. Expand from spacy's
    `Token.is_digit` and `Token.is_alpha` attributes.

    Parameters
    ----------
    token : Token
        One item of Doc object, representing a word, punctuation symbol, whitespace, etc.
    valid_punctuation_marks : type
        Punctuation marks that are valid for a candidate, defaults to '-'.

    Returns
    -------
    bool
        Return true when token contains only only alpha-numeric
        characters and valid punctuation, otherwise, return False.
    """
    for punct in valid_punctuation_marks.split():
        word = token.lemma_.replace(punct, '')
    return word.isalnum()
