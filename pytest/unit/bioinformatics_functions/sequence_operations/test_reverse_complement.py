import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.sequence_operations.reverse_complement import (
        reverse_complement,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    reverse_complement = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_reverse_complement_basic() -> None:
    """
    Test case 1: Basic reverse complement of DNA sequence.
    """
    seq = "ATGC"
    result = reverse_complement(seq)
    assert result == "GCAT"


def test_reverse_complement_longer_sequence() -> None:
    """
    Test case 2: Reverse complement of longer sequence.
    """
    seq = "ATGCATGC"
    result = reverse_complement(seq)
    assert result == "GCATGCAT"


def test_reverse_complement_lowercase() -> None:
    """
    Test case 3: Lowercase input sequence.
    """
    seq = "atgc"
    result = reverse_complement(seq)
    assert result == "gcat"


def test_reverse_complement_empty_sequence() -> None:
    """
    Test case 4: Empty sequence returns empty string.
    """
    result = reverse_complement("")
    assert result == ""


def test_reverse_complement_mixed_case() -> None:
    """
    Test case 5: Mixed case input sequence.
    """
    seq = "AtGc"
    result = reverse_complement(seq)
    assert result == "gCaT"


def test_reverse_complement_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        reverse_complement(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        reverse_complement(None)


def test_reverse_complement_invalid_base_error() -> None:
    """
    Test case 7: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        reverse_complement("ATGCX")
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        reverse_complement("ATGCU")
