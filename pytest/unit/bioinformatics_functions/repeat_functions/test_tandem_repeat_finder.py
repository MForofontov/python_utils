import pytest
from bioinformatics_functions.repeat_functions.tandem_repeat_finder import tandem_repeat_finder


def test_tandem_repeat_finder_basic() -> None:
    """
    Test case 1: Basic tandem repeat finding.
    """
    sequence = "ATATATGC"
    result = tandem_repeat_finder(sequence, min_repeat=2, min_length=2)
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) for item in result)
    assert all(len(item) == 3 for item in result)


def test_tandem_repeat_finder_no_repeats() -> None:
    """
    Test case 2: No tandem repeats found.
    """
    sequence = "ATGC"
    result = tandem_repeat_finder(sequence, min_repeat=2, min_length=2)
    assert result == []


def test_tandem_repeat_finder_multiple_repeats() -> None:
    """
    Test case 3: Multiple tandem repeats.
    """
    sequence = "ATATAGCGCGC"
    result = tandem_repeat_finder(sequence, min_repeat=2, min_length=2)
    assert len(result) >= 2


def test_tandem_repeat_finder_empty_sequence() -> None:
    """
    Test case 4: Empty sequence returns empty list.
    """
    result = tandem_repeat_finder("", min_repeat=2, min_length=2)
    assert result == []


def test_tandem_repeat_finder_three_repeats() -> None:
    """
    Test case 5: Find three tandem repeats.
    """
    sequence = "ATGATGATG"
    result = tandem_repeat_finder(sequence, min_repeat=3, min_length=3)
    assert len(result) > 0


def test_tandem_repeat_finder_invalid_min_repeat_error() -> None:
    """
    Test case 6: ValueError for invalid min_repeat.
    """
    with pytest.raises(ValueError, match="min_repeat must be > 1"):
        tandem_repeat_finder("ATGC", min_repeat=1, min_length=2)
    with pytest.raises(ValueError, match="min_repeat must be > 1"):
        tandem_repeat_finder("ATGC", min_repeat=0, min_length=2)


def test_tandem_repeat_finder_invalid_min_length_error() -> None:
    """
    Test case 7: ValueError for invalid min_length.
    """
    with pytest.raises(ValueError, match="min_length must be > 0"):
        tandem_repeat_finder("ATGC", min_repeat=2, min_length=0)
    with pytest.raises(ValueError, match="min_length must be > 0"):
        tandem_repeat_finder("ATGC", min_repeat=2, min_length=-1)
