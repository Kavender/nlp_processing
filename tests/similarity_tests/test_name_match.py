import pytest
from similarity.name_match import (double_metaphone, double_metaphone_compare, Threshold, entity_similarity_token_count)


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("Smith", ("SM0", "XM0")),
        ("Johnson", ("JNSN", "")),
        ("Williams", ("WLMS", "")),
    ]
)
def test_double_metaphone(input_str, expected_output):
    assert double_metaphone(input_str) == expected_output



@pytest.mark.parametrize(
    "tuple1, tuple2, threshold, expected_output",
    [
        (("SM0", "XM0"), ("JNSN", ""), Threshold.WEAK, False),
        (("SM0", "XM0"), ("SM0", "XM0"), Threshold.NORMAL, True),
        (("SM0", "XM0"), ("SM0", ""), Threshold.STRONG, True),
    ]
)
def test_double_metaphone_compare(tuple1, tuple2, threshold, expected_output):
    assert double_metaphone_compare(tuple1, tuple2, threshold) == expected_output


@pytest.mark.parametrize(
    "e1, e2, expected_output",
    [
        ("John Doe", "John Doe", 1),
        ("John Doe", "Doe John", 1),
        ("John Doe", "Jane Doe", 0.5),
    ]
)
def test_entity_similarity_token_count(e1, e2, expected_output):
    assert entity_similarity_token_count(e1, e2) == expected_output

