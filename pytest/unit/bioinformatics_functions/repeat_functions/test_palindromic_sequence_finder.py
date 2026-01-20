import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.repeat_functions.palindromic_sequence_finder import (
        palindromic_sequence_finder,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    palindromic_sequence_finder = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


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
    Test case 5: Palindrome subsequences in sequence.
    """
    sequence = "ATTA"
    result = palindromic_sequence_finder(sequence, min_length=4)
    assert len(result) >= 1  # ATTA is a palindrome


def test_palindromic_sequence_finder_invalid_min_length_error() -> None:
    """
    Test case 6: ValueError for invalid min_length.
    """
    with pytest.raises(ValueError, match="min_length must be > 0"):
        palindromic_sequence_finder("ATGC", min_length=0)
    with pytest.raises(ValueError, match="min_length must be > 0"):
        palindromic_sequence_finder("ATGC", min_length=-1)
