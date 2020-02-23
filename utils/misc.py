# /usr/bin/env python -u
# -*- coding: utf-8 -*-
from typing import Iterable, Set, Any, List
from collections import Counter
import numpy
from sklearn.feature_extraction.text import CountVectorizer


def overlap_items(seq1: Iterable[Any], seq2: Iterable[Any]) -> Set[Any]:
    "Return the overlapped items between two sequences of data"
    return set(seq1).intersection(seq2)


def consecutive(data: Iterable[int], stepsize=1) -> Iterable[List[int]]:
    """Split the sequence of data if difference between two neighbors
    is greater than stepsize."""
    return numpy.split(data, numpy.where(numpy.diff(data) > stepsize)[0]+1)


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
    for token, count in self.items():
        if count < min_freq:
            freq += count
        else:
            filtered[token] = count
    filtered[replaced_token] = filtered.get(replaced_token, 0) + freq
    return filtered


def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    #vec1 = CountVectorizer(ngram_range=(2,2),
   #         max_features=2000).fit(corpus) #get bigrams
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                   vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]
