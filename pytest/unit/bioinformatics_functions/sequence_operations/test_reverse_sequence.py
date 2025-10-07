import pytest
from bioinformatics_functions.sequence_operations.reverse_sequence import reverse_sequence


def test_reverse_sequence_basic() -> None:
    """
    Test case 1: Basic sequence reversal.
    """
    seq = "ATGC"
    result = reverse_sequence(seq)
    assert result == "CGTA"


def test_reverse_sequence_longer() -> None:
    """
    Test case 2: Longer sequence reversal.
    """
    seq = "ATGCATGC"
    result = reverse_sequence(seq)
    assert result == "CGTACGTA"


def test_reverse_sequence_single_char() -> None:
    """
    Test case 3: Single character sequence.
    """
    seq = "A"
    result = reverse_sequence(seq)
    assert result == "A"


def test_reverse_sequence_empty() -> None:
    """
    Test case 4: Empty sequence returns empty string.
    """
    result = reverse_sequence("")
    assert result == ""


def test_reverse_sequence_palindrome() -> None:
    """
    Test case 5: Palindrome sequence.
    """
    seq = "ATCGCGTA"
    result = reverse_sequence(seq)
    assert result == "ATGCGCTA"


def test_reverse_sequence_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        reverse_sequence(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        reverse_sequence(None)
