import pytest
from bioinformatics_functions.alignment_functions.phylogenetic_distance import (
    phylogenetic_distance,
)


def test_phylogenetic_distance_typical() -> None:
    """
    Test case 1: Typical evolutionary distance calculation.
    """
    seq1 = "ATGC"
    seq2 = "ATGT"
    result = phylogenetic_distance(seq1, seq2)
    assert isinstance(result, float)
    assert result == 0.25


def test_phylogenetic_distance_identical() -> None:
    """
    Test case 2: Distance is 0.0 for identical sequences.
    """
    seq1 = "ATGC"
    seq2 = "ATGC"
    result = phylogenetic_distance(seq1, seq2)
    assert result == 0.0


def test_phylogenetic_distance_all_different() -> None:
    """
    Test case 3: Distance is 1.0 for completely different sequences.
    """
    seq1 = "AAAA"
    seq2 = "TTTT"
    result = phylogenetic_distance(seq1, seq2)
    assert result == 1.0


def test_phylogenetic_distance_empty_sequences() -> None:
    """
    Test case 4: Distance for empty sequences (should raise ValueError).
    """
    with pytest.raises(ValueError):
        phylogenetic_distance("", "")


def test_phylogenetic_distance_length_mismatch() -> None:
    """
    Test case 5: ValueError for sequences of different lengths.
    """
    with pytest.raises(ValueError):
        phylogenetic_distance("ATGC", "ATG")
