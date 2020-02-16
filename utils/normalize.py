# coding: utf-8
from __future__ import unicode_literals
import re
from typing import Union, List
from util.contractions import CONTRACTION_MAP
from utils.regex import (ENGLISH_PUNCTUATIONS, ARABIC_PUNCTUATIONS, REGEX_HYPHENATED_WORD,
                         REGEX_CONSECUTIVE_PUNCTUATION, REGEX_NEWLINE, REGEX_NONBREAKING_SPACE)


def remove_consecutive_spaces(text: str) -> str:
    """Compress multi whitespace into single space, replace multiple line-breaking
    whitespaces with a single newline, and then strip any leading/trailing whitespace."""
     return REGEX_NONBREAKING_SPACE.sub(" ", REGEX_NEWLINE.sub(r"\n", text)).strip()


def remove_punctuations(text: str, punctuations: str=ENGLISH_PUNCTUATIONS) -> str:
    translator = str.maketrans('', '', punctuations)
    return text.translate(translator)


def remove_consecutive_punctuation(text: str) -> str:
    "Remove consecutive punctuations, such as ..."
    return REGEX_CONSECUTIVE_PUNCTUATION.sub('', text)


def remove_nonascii_chars(text: str) -> str:
    """Return string with NonAscii characters removed."""
    letters = [l for l in text if ord(l) < 128 else  " "]
    return "".join(letters).strip()


def normalize_arabic(text: str) -> str:
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def normalize_hyphenated_words(text: str, keep_hyphen: bool=True):
    """Normalize words that have been split by a hyphen by joining the pieces back together."""
    if keep_hyphen:
        return "".join(split_and_keep_punctuation(text))
    else:
        return REGEX_HYPHENATED_WORD.sub(r"\1\2", text)


def split_and_keep_punctuation(text: str) -> List[str]:
    """Split text on punctuation and both string and punctuation components."""
    text_splits = re.split('([^a-zA-Z0-9])', text)
    return [sub_text.strip() for sub_text in text_splits if sub_text.strip()]


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
