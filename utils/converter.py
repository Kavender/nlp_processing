# coding: utf-8
from __future__ import unicode_literals
from math import isfinite
from word2number import w2n
from typing import Union

# TODO: add hashing functions either from pyhash or from the hashlib


def get_hex_encoding(text: str):
    return ' '.join(hex(ord(char)) for char in text)

def print_string_and_encoding(s):
    print(f'{s} : {get_hex_encoding(s)}') 


def convert_text_to_float(text: str) -> float:
    "Transform text format of float value to float."
    try:
        if isfinite(float(text)):
            return float(text)
    except (ValueError, IndexError):
        return None


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


def convert_text_to_bool(text) -> bool:
    "Transform bool type string to bool value"
    if text.lower() == "yes":
        return True
    elif text.lower() == "no":
        return False
    return None
