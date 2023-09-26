from numbers import Number
from itertools import zip_longest
from numpy.testing import assert_almost_equal
from typing import Any, Iterable, Dict


def assert_deep_almost_equal(actual: Any, expected: Any, decimal: int = 7, type_force: bool = False):
    """Check deep equality between two python data structures recursing 
    into sub-structures, including iterators and generators.
    Inspired by: https://github.com/larsbutler/oq-engine/blob/master/tests/utils/helpers.py

    Args:
        actual (Any): [description]
        expected (Any): [description]
        decimal (int, optional): [description]. Defaults to 7.

    >>> x1, y1 = ({'a': 'b', 'num': 0.15}, {'a': 'b', 'num': 0.150000002})
    >>> assert_deep_almost_equal(x1, y1)
    >>> x2, y2 = (['a', 'b', ['a', 'b']], [u'a', u'b', [u'a', u'b']])
    >>> assert_deep_almost_equal(x2, y2)
    >>> x3, y3 = ({'c': (0.99999998, 'similarity'), 'a': {'b': 'c'}}, {'a': {'b': 'c'}, 'c': (1.00000006, 'similarity')})
    >>> assert_deep_almost_equal(x3, y3)
    >>> assert_deep_almost_equal((str(p) for p in range(10)), (str(p) for p in range(10)))
    """
    if type_force:
        assert type(actual) == type(expected), f"Expect to have {type(expected)} type but found {type(actual)}."

    if isinstance(expected, Number):
        assert_almost_equal(actual, expected, decimal=decimal)
    elif isinstance(expected, Dict):
        # TODO: consider us our customerized sorting function, to avoid randomness when sort two same length similar nps in key
        assert sorted(actual.keys()) == sorted(expected.keys())
        for key, expected_val in expected.items():
            assert_deep_almost_equal(actual[key], expected_val, decimal=decimal, type_force=type_force)
    elif isinstance(expected, Iterable) and not isinstance(expected, str):
        for actual_val, expected_val in zip_longest(actual, expected, fillvalue=object()):
            assert_deep_almost_equal(actual_val, expected_val, decimal=decimal, type_force=type_force)
    else:
        assert actual == expected


if __name__ == "__main__":
    import doctest

    doctest.testmod()
