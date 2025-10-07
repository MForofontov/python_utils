import pytest
from bioinformatics_functions.repeat_functions.palindromic_sequence_finder import palindromic_sequence_finder


def test_palindromic_sequence_finder_basic() -> None:
    """
    Test case 1: Basic palindrome finding in sequence.
    """
    sequence = "ATGCAT"
    result = palindromic_sequence_finder(sequence, min_length=4)
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) for item in result)
    assert all(len(item) == 3 for item in result)


def test_palindromic_sequence_finder_no_palindromes() -> None:
    """
    Test case 2: No palindromes found.
    """
    sequence = "ATGCA"
    result = palindromic_sequence_finder(sequence, min_length=4)
    assert result == []


def test_palindromic_sequence_finder_short_palindrome() -> None:
    """
    Test case 3: Find short palindromes with min_length=2.
    """
    sequence = "ATTA"
    result = palindromic_sequence_finder(sequence, min_length=2)
    assert len(result) > 0


def test_palindromic_sequence_finder_empty_sequence() -> None:
    """
    Test case 4: Empty sequence returns empty list.
    """
    result = palindromic_sequence_finder("", min_length=4)
    assert result == []


def test_palindromic_sequence_finder_entire_palindrome() -> None:
    """
    Test case 5: Entire sequence is palindrome.
    """
    sequence = "ATCGCGAT"
    result = palindromic_sequence_finder(sequence, min_length=8)
    assert any(item[2] == sequence for item in result)


def test_palindromic_sequence_finder_invalid_min_length_error() -> None:
    """
    Test case 6: ValueError for invalid min_length.
    """
    with pytest.raises(ValueError, match="min_length must be > 0"):
        palindromic_sequence_finder("ATGC", min_length=0)
    with pytest.raises(ValueError, match="min_length must be > 0"):
        palindromic_sequence_finder("ATGC", min_length=-1)
