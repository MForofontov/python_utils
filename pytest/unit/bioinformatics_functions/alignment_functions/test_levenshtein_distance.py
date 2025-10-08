import pytest
from bioinformatics_functions.alignment_functions.levenshtein_distance import levenshtein_distance


def test_levenshtein_distance_identical() -> None:
    """Test distance between identical sequences."""
    assert levenshtein_distance("ACGT", "ACGT") == 0


def test_levenshtein_distance_one_substitution() -> None:
    """Test distance with one substitution."""
    assert levenshtein_distance("ACGT", "ACCT") == 1


def test_levenshtein_distance_one_deletion() -> None:
    """Test distance with one deletion."""
    assert levenshtein_distance("ACGT", "ACT") == 1


def test_levenshtein_distance_one_insertion() -> None:
    """Test distance with one insertion."""
    assert levenshtein_distance("ACT", "ACGT") == 1


def test_levenshtein_distance_multiple_edits() -> None:
    """Test distance with multiple edits."""
    # "kitten" -> "sitting" requires 3 edits
    assert levenshtein_distance("kitten", "sitting") == 3


def test_levenshtein_distance_empty_to_nonempty() -> None:
    """Test distance from empty to non-empty sequence."""
    assert levenshtein_distance("", "ABC") == 3
    assert levenshtein_distance("ABC", "") == 3


def test_levenshtein_distance_both_empty() -> None:
    """Test distance between empty sequences."""
    assert levenshtein_distance("", "") == 0


def test_levenshtein_distance_completely_different() -> None:
    """Test distance between completely different sequences."""
    result = levenshtein_distance("AAAA", "TTTT")
    assert result == 4


def test_levenshtein_distance_seq1_type_error() -> None:
    """Test TypeError for non-string seq1."""
    with pytest.raises(TypeError, match="seq1 must be a string"):
        levenshtein_distance(123, "ACGT")


def test_levenshtein_distance_seq2_type_error() -> None:
    """Test TypeError for non-string seq2."""
    with pytest.raises(TypeError, match="seq2 must be a string"):
        levenshtein_distance("ACGT", 123)
