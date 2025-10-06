import pytest
from bioinformatics_functions.gc_functions.gc_content import gc_content


def test_gc_content_typical() -> None:
    """
    Test case 1: Typical GC content calculation.
    """
    seq = "ATGC"
    result = gc_content(seq)
    assert isinstance(result, float)
    assert result == 50.0


def test_gc_content_all_gc() -> None:
    """
    Test case 2: Sequence with only G and C.
    """
    seq = "GGCC"
    result = gc_content(seq)
    assert result == 100.0


def test_gc_content_no_gc() -> None:
    """
    Test case 3: Sequence with no G or C.
    """
    seq = "ATAT"
    result = gc_content(seq)
    assert result == 0.0


def test_gc_content_empty() -> None:
    """
    Test case 4: Empty sequence returns 0.0.
    """
    seq = ""
    result = gc_content(seq)
    assert result == 0.0


def test_gc_content_type_error() -> None:
    """
    Test case 5: TypeError for non-string input.
    """
    with pytest.raises(TypeError):
        gc_content(123)


def test_gc_content_value_error() -> None:
    """
    Test case 6: ValueError for invalid characters.
    """
    with pytest.raises(ValueError):
        gc_content("ATXG")
