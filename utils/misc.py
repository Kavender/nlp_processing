from typing import Iterable, Set, Any, List
from collections import Counter

def overlap_items(seq1: Iterable[Any], seq2: Iterable[Any]) -> Set[Any]:
    "Return the overlapped items between two sequences of data"
    return set(seq1).intersection(seq2)

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
