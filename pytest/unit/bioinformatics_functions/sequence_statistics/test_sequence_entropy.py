import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.sequence_statistics.sequence_entropy import (
        sequence_entropy,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    sequence_entropy = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_sequence_entropy_uniform() -> None:
    """
    Test case 1: Uniform distribution has maximum entropy.
    """
    seq = "ATGC"
    result = sequence_entropy(seq)
    assert result == 2.0


def test_sequence_entropy_all_same() -> None:
    """
    Test case 2: All same bases has zero entropy.
    """
    seq = "AAAA"
    result = sequence_entropy(seq)
    assert result == 0.0


def test_sequence_entropy_two_bases() -> None:
    """
    Test case 3: Two different bases.
    """
    seq = "AATT"
    result = sequence_entropy(seq)
    assert result == 1.0


def test_sequence_entropy_longer_sequence() -> None:
    """
    Test case 4: Longer sequence entropy.
    """
    seq = "ATGCATGCATGC"
    result = sequence_entropy(seq)
    assert isinstance(result, float)
    assert result > 0


def test_sequence_entropy_single_char() -> None:
    """
    Test case 5: Single character has zero entropy.
    """
    seq = "A"
    result = sequence_entropy(seq)
    assert result == 0.0


def test_sequence_entropy_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        sequence_entropy(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        sequence_entropy(None)


def test_sequence_entropy_empty_error() -> None:
    """
    Test case 7: ValueError for empty sequence.
    """
    with pytest.raises(ValueError, match="Sequence must not be empty"):
        sequence_entropy("")
