import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.gc_functions.gc_skew import gc_skew
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    gc_skew = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_gc_skew_equal_g_and_c() -> None:
    """
    Test case 1: Equal G and C bases returns 0.0.
    """
    seq = "GGCC"
    result = gc_skew(seq)
    assert result == 0.0


def test_gc_skew_more_g_than_c() -> None:
    """
    Test case 2: More G than C returns positive skew.
    """
    seq = "GGGCC"
    result = gc_skew(seq)
    assert result > 0


def test_gc_skew_more_c_than_g() -> None:
    """
    Test case 3: More C than G returns negative skew.
    """
    seq = "GGCCC"
    result = gc_skew(seq)
    assert result < 0


def test_gc_skew_lowercase() -> None:
    """
    Test case 4: Lowercase input sequence.
    """
    seq = "ggcc"
    result = gc_skew(seq)
    assert result == 0.0


def test_gc_skew_with_at_bases() -> None:
    """
    Test case 5: Sequence with A and T bases (ignored in calculation).
    """
    seq = "ATGGGCCAT"
    result = gc_skew(seq)
    assert result > 0


def test_gc_skew_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        gc_skew(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        gc_skew(None)


def test_gc_skew_invalid_base_error() -> None:
    """
    Test case 7: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        gc_skew("ATGCX")


def test_gc_skew_no_gc_bases_error() -> None:
    """
    Test case 8: ValueError for no G or C bases.
    """
    with pytest.raises(ValueError, match="No G or C bases in sequence"):
        gc_skew("ATAT")
