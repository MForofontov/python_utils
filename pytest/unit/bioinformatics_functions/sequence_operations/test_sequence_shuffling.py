import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.sequence_operations.sequence_shuffling import (
        sequence_shuffling,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    sequence_shuffling = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_sequence_shuffling_basic() -> None:
    """
    Test case 1: Basic sequence shuffling preserves length.
    """
    sequence = "ATGC"
    result = sequence_shuffling(sequence)
    assert isinstance(result, str)
    assert len(result) == len(sequence)


def test_sequence_shuffling_preserves_composition() -> None:
    """
    Test case 2: Shuffling preserves sequence composition.
    """
    sequence = "AAATTGGGCCC"
    result = sequence_shuffling(sequence)
    assert sorted(result) == sorted(sequence)


def test_sequence_shuffling_single_char() -> None:
    """
    Test case 3: Single character returns same character.
    """
    sequence = "A"
    result = sequence_shuffling(sequence)
    assert result == "A"


def test_sequence_shuffling_empty() -> None:
    """
    Test case 4: Empty sequence returns empty string.
    """
    result = sequence_shuffling("")
    assert result == ""


def test_sequence_shuffling_all_same() -> None:
    """
    Test case 5: All same characters.
    """
    sequence = "AAAA"
    result = sequence_shuffling(sequence)
    assert result == "AAAA"


def test_sequence_shuffling_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="sequence must be a string"):
        sequence_shuffling(12345)
    with pytest.raises(TypeError, match="sequence must be a string"):
        sequence_shuffling(None)
