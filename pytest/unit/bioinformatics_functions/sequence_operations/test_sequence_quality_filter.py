import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.sequence_operations.sequence_quality_filter import (
    sequence_quality_filter,
)


def test_sequence_quality_filter_passes_all() -> None:
    """Test case 1: Test sequence that passes all filters."""
    result = sequence_quality_filter("ATGCATGC", min_length=5, max_gc=60.0)
    assert result["passes_filter"] is True
    assert result["length"] == 8
    assert result["gc_content"] == 50.0
    assert result["failed_filters"] == []


def test_sequence_quality_filter_fails_min_length() -> None:
    """Test case 2: Test sequence failing minimum length filter."""
    result = sequence_quality_filter("AT", min_length=5)
    assert result["passes_filter"] is False
    assert "min_length" in result["failed_filters"]


def test_sequence_quality_filter_fails_max_length() -> None:
    """Test case 3: Test sequence failing maximum length filter."""
    result = sequence_quality_filter("ATGCATGCATGC", max_length=8)
    assert result["passes_filter"] is False
    assert "max_length" in result["failed_filters"]


def test_sequence_quality_filter_fails_gc_content() -> None:
    """Test case 4: Test sequence failing GC content filters."""
    # GGGGCCCC is 100% GC
    result = sequence_quality_filter("GGGGCCCC", max_gc=50.0)
    assert result["passes_filter"] is False
    assert "max_gc" in result["failed_filters"]


def test_sequence_quality_filter_n_content() -> None:
    """Test case 5: Test sequence with N content."""
    result = sequence_quality_filter("NNNATGC", max_n_content=20.0)
    assert result["passes_filter"] is False
    assert result["n_content"] > 20.0
    assert "max_n_content" in result["failed_filters"]


def test_sequence_quality_filter_no_filters() -> None:
    """Test case 6: Test with no filters applied."""
    result = sequence_quality_filter("ATGC")
    assert result["passes_filter"] is True
    assert result["failed_filters"] == []


def test_sequence_quality_filter_invalid_min_max() -> None:
    """Test case 7: Test ValueError for min > max."""
    with pytest.raises(
        ValueError, match="min_length .* cannot be greater than max_length"
    ):
        sequence_quality_filter("ATGC", min_length=10, max_length=5)


def test_sequence_quality_filter_type_error() -> None:
    """Test case 8: Test TypeError for non-string seq."""
    with pytest.raises(TypeError, match="seq must be a string"):
        sequence_quality_filter(123)


def test_sequence_quality_filter_param_type_error() -> None:
    """Test case 9: Test TypeError for non-numeric parameter."""
    with pytest.raises(TypeError, match="min_length must be a number or None"):
        sequence_quality_filter("ATGC", min_length="five")


def test_sequence_quality_filter_negative_min_length() -> None:
    """Test case 10: Test ValueError for negative min_length."""
    with pytest.raises(ValueError, match="min_length must be non-negative"):
        sequence_quality_filter("ATGC", min_length=-5)


def test_sequence_quality_filter_negative_max_length() -> None:
    """Test case 11: Test ValueError for negative max_length."""
    with pytest.raises(ValueError, match="max_length must be non-negative"):
        sequence_quality_filter("ATGC", max_length=-10)


def test_sequence_quality_filter_gc_content_range() -> None:
    """Test case 12: Test ValueError for GC content out of range."""
    with pytest.raises(ValueError, match="min_gc must be between 0 and 100"):
        sequence_quality_filter("ATGC", min_gc=150.0)


def test_sequence_quality_filter_max_n_content_range() -> None:
    """Test case 13: Test ValueError for max_n_content out of range."""
    with pytest.raises(ValueError, match="max_n_content must be between 0 and 100"):
        sequence_quality_filter("ATGC", max_n_content=200.0)


def test_sequence_quality_filter_min_gc_greater_than_max_gc() -> None:
    """Test case 14: Test ValueError when min_gc > max_gc."""
    with pytest.raises(ValueError, match="min_gc .* cannot be greater than max_gc"):
        sequence_quality_filter("ATGC", min_gc=60.0, max_gc=40.0)
