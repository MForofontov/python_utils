import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.gc_functions.sequence_gc_profile import (
    sequence_gc_profile,
)


def test_sequence_gc_profile_basic() -> None:
    """
    Test case 1: Basic GC profile calculation.
    """
    seq = "ATGCGCGT"
    result = sequence_gc_profile(seq, 4)
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)
    assert len(result) == 5


def test_sequence_gc_profile_all_gc() -> None:
    """
    Test case 2: All GC bases returns 100%.
    """
    seq = "GGCC"
    result = sequence_gc_profile(seq, 4)
    assert result == [100.0]


def test_sequence_gc_profile_no_gc() -> None:
    """
    Test case 3: No GC bases returns 0%.
    """
    seq = "ATAT"
    result = sequence_gc_profile(seq, 4)
    assert result == [0.0]


def test_sequence_gc_profile_window_two() -> None:
    """
    Test case 4: Window size of 2.
    """
    seq = "ATGC"
    result = sequence_gc_profile(seq, 2)
    assert len(result) == 3


def test_sequence_gc_profile_window_equals_length() -> None:
    """
    Test case 5: Window size equals sequence length.
    """
    seq = "ATGC"
    result = sequence_gc_profile(seq, 4)
    assert len(result) == 1
    assert result[0] == 50.0


def test_sequence_gc_profile_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        sequence_gc_profile(12345, 4)
    with pytest.raises(TypeError, match="window must be int"):
        sequence_gc_profile("ATGC", 4.5)


def test_sequence_gc_profile_invalid_value_error() -> None:
    """
    Test case 7: ValueError for invalid values.
    """
    with pytest.raises(ValueError, match="window must be positive"):
        sequence_gc_profile("ATGC", 0)
    with pytest.raises(ValueError, match="window cannot be longer than sequence"):
        sequence_gc_profile("ATGC", 5)


def test_sequence_gc_profile_invalid_base_error() -> None:
    """
    Test case 8: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        sequence_gc_profile("ATGCX", 4)
