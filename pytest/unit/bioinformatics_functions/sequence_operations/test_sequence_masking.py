import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.sequence_operations.sequence_masking import (
        sequence_masking,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    sequence_masking = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_sequence_masking_basic() -> None:
    """
    Test case 1: Basic sequence masking of runs.
    """
    seq = "AAATTTCCCGGG"
    result = sequence_masking(seq, mask_char="N", threshold=3)
    assert isinstance(result, str)
    assert "N" in result


def test_sequence_masking_no_masking() -> None:
    """
    Test case 2: No runs to mask.
    """
    seq = "ATGC"
    result = sequence_masking(seq, mask_char="N", threshold=3)
    assert result == "ATGC"


def test_sequence_masking_custom_mask_char() -> None:
    """
    Test case 3: Custom mask character.
    """
    seq = "AAAA"
    result = sequence_masking(seq, mask_char="X", threshold=3)
    assert "X" in result


def test_sequence_masking_threshold_one() -> None:
    """
    Test case 4: Threshold of 1 masks all identical runs.
    """
    seq = "AATGC"
    result = sequence_masking(seq, mask_char="N", threshold=2)
    assert result == "NNTGC"


def test_sequence_masking_empty_sequence() -> None:
    """
    Test case 5: Empty sequence returns empty string.
    """
    result = sequence_masking("", mask_char="N", threshold=3)
    assert result == ""


def test_sequence_masking_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        sequence_masking(12345, mask_char="N", threshold=3)
    with pytest.raises(TypeError, match="mask_char must be str"):
        sequence_masking("ATGC", mask_char=123, threshold=3)
    with pytest.raises(TypeError, match="threshold must be int"):
        sequence_masking("ATGC", mask_char="N", threshold=3.5)


def test_sequence_masking_invalid_value_error() -> None:
    """
    Test case 7: ValueError for invalid values.
    """
    with pytest.raises(ValueError, match="threshold must be >= 1"):
        sequence_masking("ATGC", mask_char="N", threshold=0)
    with pytest.raises(ValueError, match="mask_char must not be empty"):
        sequence_masking("ATGC", mask_char="", threshold=3)
