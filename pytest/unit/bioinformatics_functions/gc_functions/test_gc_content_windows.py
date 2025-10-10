import pytest
from bioinformatics_functions.gc_functions.gc_content_windows import gc_content_windows


def test_gc_content_windows_non_overlapping() -> None:
    """Test case 1: Test non-overlapping windows."""
    result = gc_content_windows("ATGCATGCATGC", window_size=4, step_size=4)
    assert len(result) == 3
    assert result[0] == (0, 4, 50.0)
    assert result[1] == (4, 8, 50.0)
    assert result[2] == (8, 12, 50.0)


def test_gc_content_windows_overlapping() -> None:
    """Test case 2: Test overlapping windows."""
    result = gc_content_windows("ATGCATGC", window_size=4, step_size=2)
    assert len(result) == 3
    # Windows at positions 0, 2, 4
    assert result[0][0] == 0
    assert result[1][0] == 2
    assert result[2][0] == 4


def test_gc_content_windows_default_step() -> None:
    """Test case 3: Test default step size (non-overlapping)."""
    result = gc_content_windows("ATGCATGC", window_size=4)
    assert len(result) == 2
    assert result[0] == (0, 4, 50.0)
    assert result[1] == (4, 8, 50.0)


def test_gc_content_windows_all_gc() -> None:
    """Test case 4: Test window with 100% GC content."""
    result = gc_content_windows("GGGGCCCC", window_size=4, step_size=4)
    assert result[0][2] == 100.0
    assert result[1][2] == 100.0


def test_gc_content_windows_no_gc() -> None:
    """Test case 5: Test window with 0% GC content."""
    result = gc_content_windows("AAAATTTT", window_size=4, step_size=4)
    assert result[0][2] == 0.0
    assert result[1][2] == 0.0


def test_gc_content_windows_too_short() -> None:
    """Test case 6: Test ValueError for sequence shorter than window."""
    with pytest.raises(
        ValueError, match="Sequence length .* must be at least window_size"
    ):
        gc_content_windows("ATG", window_size=10)


def test_gc_content_windows_invalid_window_size() -> None:
    """Test case 7: Test ValueError for window size less than 1."""
    with pytest.raises(ValueError, match="window_size must be at least 1"):
        gc_content_windows("ATGCATGC", window_size=0)


def test_gc_content_windows_invalid_step_size() -> None:
    """Test case 8: Test ValueError for step size less than 1."""
    with pytest.raises(ValueError, match="step_size must be at least 1"):
        gc_content_windows("ATGCATGC", window_size=4, step_size=0)


def test_gc_content_windows_type_error() -> None:
    """Test case 9: Test TypeError for non-string seq."""
    with pytest.raises(TypeError, match="seq must be a string"):
        gc_content_windows(123)
