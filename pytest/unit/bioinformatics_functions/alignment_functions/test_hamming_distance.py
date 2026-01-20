import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.alignment_functions.hamming_distance import (
        hamming_distance,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    hamming_distance = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_hamming_distance_no_difference() -> None:
    """
    Test case 1: Identical sequences return 0.
    """
    seq1 = "ATGC"
    seq2 = "ATGC"
    result = hamming_distance(seq1, seq2)
    assert result == 0


def test_hamming_distance_one_difference() -> None:
    """
    Test case 2: One difference returns 1.
    """
    seq1 = "ATGC"
    seq2 = "ATGT"
    result = hamming_distance(seq1, seq2)
    assert result == 1


def test_hamming_distance_all_different() -> None:
    """
    Test case 3: All positions different.
    """
    seq1 = "ATGC"
    seq2 = "GCTA"
    result = hamming_distance(seq1, seq2)
    assert result == 4


def test_hamming_distance_longer_sequences() -> None:
    """
    Test case 4: Longer sequences with multiple differences.
    """
    seq1 = "ATGCATGC"
    seq2 = "ATGTATGC"
    result = hamming_distance(seq1, seq2)
    assert result == 1


def test_hamming_distance_single_base() -> None:
    """
    Test case 5: Single base sequences.
    """
    seq1 = "A"
    seq2 = "T"
    result = hamming_distance(seq1, seq2)
    assert result == 1


def test_hamming_distance_empty_sequences() -> None:
    """
    Test case 6: Empty sequences return 0.
    """
    result = hamming_distance("", "")
    assert result == 0


def test_hamming_distance_invalid_type_error() -> None:
    """
    Test case 7: TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="seq1 must be str"):
        hamming_distance(12345, "ATGC")
    with pytest.raises(TypeError, match="seq2 must be str"):
        hamming_distance("ATGC", 12345)


def test_hamming_distance_different_length_error() -> None:
    """
    Test case 8: ValueError for different length sequences.
    """
    with pytest.raises(ValueError, match="Sequences must be the same length"):
        hamming_distance("ATGC", "ATG")
    with pytest.raises(ValueError, match="Sequences must be the same length"):
        hamming_distance("ATG", "ATGC")
