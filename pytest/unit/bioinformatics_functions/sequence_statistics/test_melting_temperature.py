import pytest
from bioinformatics_functions.sequence_statistics.melting_temperature import melting_temperature


def test_melting_temperature_basic() -> None:
    """
    Test case 1: Basic melting temperature calculation.
    """
    seq = "ATGC"
    result = melting_temperature(seq)
    assert isinstance(result, float)
    assert result > 0


def test_melting_temperature_short_sequence() -> None:
    """
    Test case 2: Short sequence (<14 bases) uses simple formula.
    """
    seq = "ATGCATGC"
    result = melting_temperature(seq)
    assert isinstance(result, float)
    # AT = 4, GC = 4, so Tm = 2*4 + 4*4 = 24
    assert result == 24.0


def test_melting_temperature_long_sequence() -> None:
    """
    Test case 3: Longer sequence (>=14 bases) uses complex formula.
    """
    seq = "ATGCATGCATGCAT"
    result = melting_temperature(seq)
    assert isinstance(result, float)
    assert result > 0


def test_melting_temperature_all_gc() -> None:
    """
    Test case 4: All GC bases (higher Tm).
    """
    seq = "GGCC"
    result = melting_temperature(seq)
    assert result > 0
    # Short: 4*4 = 16
    assert result == 16.0


def test_melting_temperature_all_at() -> None:
    """
    Test case 5: All AT bases (lower Tm).
    """
    seq = "AATT"
    result = melting_temperature(seq)
    # Short: 2*4 = 8
    assert result == 8.0


def test_melting_temperature_lowercase() -> None:
    """
    Test case 6: Lowercase input sequence.
    """
    seq = "atgc"
    result = melting_temperature(seq)
    assert isinstance(result, float)
    assert result > 0


def test_melting_temperature_invalid_type_error() -> None:
    """
    Test case 7: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        melting_temperature(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        melting_temperature(None)


def test_melting_temperature_empty_error() -> None:
    """
    Test case 8: ValueError for empty or too short sequence.
    """
    with pytest.raises(ValueError, match="Sequence must be at least 2 bases long"):
        melting_temperature("")
    with pytest.raises(ValueError, match="Sequence must be at least 2 bases long"):
        melting_temperature("A")


def test_melting_temperature_invalid_base_error() -> None:
    """
    Test case 9: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        melting_temperature("ATGCX")
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        melting_temperature("ATGCU")
