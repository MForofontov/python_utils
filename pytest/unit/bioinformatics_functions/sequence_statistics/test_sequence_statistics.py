import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.sequence_statistics.sequence_statistics import (
    sequence_statistics,
)


def test_sequence_statistics_basic() -> None:
    """
    Test case 1: Basic sequence statistics.
    """
    seq = "ATGC"
    result = sequence_statistics(seq)
    assert result["length"] == 4.0
    assert result["gc_content"] == 50.0
    assert result["at_content"] == 50.0


def test_sequence_statistics_all_gc() -> None:
    """
    Test case 2: All GC bases.
    """
    seq = "GGCC"
    result = sequence_statistics(seq)
    assert result["gc_content"] == 100.0
    assert result["at_content"] == 0.0


def test_sequence_statistics_all_at() -> None:
    """
    Test case 3: All AT bases.
    """
    seq = "AATT"
    result = sequence_statistics(seq)
    assert result["gc_content"] == 0.0
    assert result["at_content"] == 100.0


def test_sequence_statistics_empty() -> None:
    """
    Test case 4: Empty sequence.
    """
    seq = ""
    result = sequence_statistics(seq)
    assert result["length"] == 0.0
    assert result["gc_content"] == 0.0
    assert result["at_content"] == 0.0


def test_sequence_statistics_lowercase() -> None:
    """
    Test case 5: Lowercase sequence.
    """
    seq = "atgc"
    result = sequence_statistics(seq)
    assert result["length"] == 4.0
    assert result["gc_content"] == 50.0


def test_sequence_statistics_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        sequence_statistics(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        sequence_statistics(None)


def test_sequence_statistics_invalid_base_error() -> None:
    """
    Test case 7: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        sequence_statistics("ATGCX")
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        sequence_statistics("ATGCU")
