# /usr/bin/env python -u
# -*- coding: utf-8 -*-
from typing import Iterable, Set, Any, List
from collections import Counter
import numpy
import string
import random
from sklearn.feature_extraction.text import CountVectorizer


def generate_short_id(length: int = 8, digit_only: bool=False) -> str:
    """Generate a short id of given length"""
    if digit_only:
        letters = string.digits
    else:   
        letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for i in range(length))


# TODO: Add function to generate a hash of a string
def generate_hash(string: str) -> str:
    """Generate a hash of a string"""
    return None


def normalize_data_range(num: float, input_min: float, input_max: float, output_min: float, output_max: float) -> float:
    """Convert the value of input from input range to output range
    """
    if input_min == input_max or output_min == output_max:
        raise VauleError("Please provide a legit boundary from input/output distributinon")
    return (num - input_min) * (output_max - output_min) / (input_max - input_min) + output_min


def rolling_pairs(iterable: Iterable[Any]) -> List[Any]:
    """Get pair of items seq-> [(item0, item1), (item1, item2), ...(itemN-1, itemN)]
    """
    return list(tuple(iterable[i : i + 2]) for i in range(len(iterable) - 1))


def overlap_items(seq1: Iterable[Any], seq2: Iterable[Any]) -> Set[Any]:
    "Return the overlapped items between two sequences of data"
    return set(seq1).intersection(seq2)


def consecutive(data: Iterable[int], stepsize=1) -> Iterable[List[int]]:
    """Split the sequence of data if difference between two neighbors
    is greater than stepsize."""
    return numpy.split(data, numpy.where(numpy.diff(data) > stepsize)[0] + 1)


def count_tokens(tokens: List[str], to_lower=False, counter=None) -> Counter:
    """
    counter: If is None, return a new Counter instance, else update Counter
    instance with the counts of `tokens`..
    """
    if to_lower:
        tokens = [t.lower() for t in tokens]

    if counter is None:
        return Counter(tokens)
    else:
        counter.update(tokens)
        return counter


def filter_counter(min_freq: int, replaced_token: str) -> Counter:
    """Replace below min_freq tokens into `replaced_token` and aggregate the
    total counts."""
    freq = 0
    filtered = Counter({})
    for token, count in filtered.items():
        if count < min_freq:
            freq += count
        else:
            filtered[token] = count
    filtered[replaced_token] = filtered.get(replaced_token, 0) + freq
    return filtered


def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    # vec1 = CountVectorizer(ngram_range=(2,2),
    #         max_features=2000).fit(corpus) #get bigrams
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]
