import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.sequence_statistics.sequence_complexity import (
        sequence_complexity,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    sequence_complexity = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_sequence_complexity_basic() -> None:
    """
    Test case 1: Basic sequence complexity calculation.
    """
    sequence = "ATGCATGC"
    result = sequence_complexity(sequence, window=4)
    assert isinstance(result, float)
    assert 0 <= result <= 1


def test_sequence_complexity_low_complexity() -> None:
    """
    Test case 2: Low complexity sequence (all same).
    """
    sequence = "AAAAAAAAAA"
    result = sequence_complexity(sequence, window=5)
    assert result < 1.0


def test_sequence_complexity_high_complexity() -> None:
    """
    Test case 3: High complexity sequence (all different).
    """
    sequence = "ATGCTAGCTAGCTACG"
    result = sequence_complexity(sequence, window=3)
    assert result > 0


def test_sequence_complexity_small_window() -> None:
    """
    Test case 4: Small window size.
    """
    sequence = "ATGC"
    result = sequence_complexity(sequence, window=2)
    assert 0 <= result <= 1


def test_sequence_complexity_window_one() -> None:
    """
    Test case 5: Window size of 1.
    """
    sequence = "ATGC"
    result = sequence_complexity(sequence, window=1)
    assert result > 0


def test_sequence_complexity_empty_error() -> None:
    """
    Test case 6: ValueError for empty sequence.
    """
    with pytest.raises(ValueError, match="sequence cannot be empty"):
        sequence_complexity("", window=4)


def test_sequence_complexity_invalid_window_error() -> None:
    """
    Test case 7: ValueError for invalid window.
    """
    with pytest.raises(ValueError, match="window must be positive"):
        sequence_complexity("ATGC", window=0)
    with pytest.raises(ValueError, match="window must be positive"):
        sequence_complexity("ATGC", window=-1)
