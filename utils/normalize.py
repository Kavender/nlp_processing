# coding: utf-8
from __future__ import unicode_literals
from typing import Union, List, Iterable
import re
import unicodedata
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


def split_and_keep_punctuation(text: str) -> List[str]:
    """Split text on punctuation and both string and punctuation components."""
    text_splits = re.split('([^a-zA-Z0-9])', text)
    return [sub_text.strip() for sub_text in text_splits if sub_text.strip()]


def remove_consecutive_punctuation(text: str) -> str:
    "Remove consecutive punctuations, such as ..."
    return REGEX_CONSECUTIVE_PUNCTUATION.sub('', text)


def remove_recurring_chars(text):
    return re.sub(r'(.)\1+', r'\1', text)


def remove_nonascii_chars(text: str) -> str:
    """Return string with NonAscii characters removed."""
    letters = [l for l in text if ord(l) < 128 else  " "]
    return "".join(letters).strip()


def remove_stopwords_from_text(text: str, tokenizer: callable, stopwords: Iterable[str],
                     check_lower_case=False):
    # # instead of join by with hyphen, it's better to call the tokenizer without split on hyphen
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if check_lower_case:
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
    else:
        filtered_tokens = [token for token in tokens if token not in stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def normalize_arabic(text: str) -> str:
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def normalize_unicode_to_ascii(text: str) -> str:
    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    val = normal.decode("utf-8")
    val = val.lower()
    # remove special characters
    val = re.sub('[^A-Za-z0-9 ]+', ' ', val)
    # remove multiple spaces
    val = re.sub(' +', ' ', val)
    return val


def normalize_hyphenated_words(text: str, keep_hyphen: bool=True):
    """Normalize words that have been split by a hyphen by joining the pieces back together."""
    if keep_hyphen:
        return "".join(split_and_keep_punctuation(text))
    else:
        return REGEX_HYPHENATED_WORD.sub(r"\1\2", text)


def expand_contractions(text: str, contraction_mapping=CONTRACTION_MAP) -> str:
    """Expand constraction expression in sentence to multigrams, to better
    catch the meaning before tokenziation.
    e.g. `hasn't` to `has not` to realize the negation signal."""
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE|re.DOTALL)
    def _expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(_expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

