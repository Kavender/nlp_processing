# coding: utf-8
from __future__ import unicode_literals
import re
import string

PUNCTUATION_REGEX = re.compile('[{0}]'.format(re.escape(string.punctuation)))


def remove_multiple_spaces(text: str) -> str:
    "Compress multi whitespace into single space."
    return re.sub("\s\s+", " ", text)


def remove_punctuation(text: str, all: bool=False):
    """
    all: Remove all punctuation. If False, only removes punctuation from
        the ends of the string.
    Returns: string with punctuation removed.
    """
    if all:
        return PUNCTUATION_REGEX.sub('', s.strip())
    else:
        return s.strip().strip(string.punctuation)
