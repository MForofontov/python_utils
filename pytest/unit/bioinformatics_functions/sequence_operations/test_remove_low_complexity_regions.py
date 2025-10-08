import pytest
from bioinformatics_functions.sequence_operations.remove_low_complexity_regions import remove_low_complexity_regions


def test_remove_low_complexity_regions_repetitive() -> None:
    """Test removal of repetitive sequence."""
    # ATG repeated many times is low complexity
    result = remove_low_complexity_regions("ATGATGATGATGATG")
    # Should be masked with N
    assert 'N' in result


def test_remove_low_complexity_regions_high_complexity() -> None:
    """Test high complexity sequence remains unchanged."""
    # Diverse sequence should pass
    seq = "ATGCTAGCTAGC"
    result = remove_low_complexity_regions(seq, window_size=4, complexity_threshold=1.0)
    assert result == seq


def test_remove_low_complexity_regions_partial() -> None:
    """Test partial masking of sequence."""
    # AAAAAA is low complexity, TGCATGC is higher
    result = remove_low_complexity_regions("AAAAAATGCATGC", window_size=5, complexity_threshold=1.0)
    # First part should be masked
    assert result.startswith('N')
    assert 'TGCATGC' in result or result.endswith('ATGC')


def test_remove_low_complexity_regions_custom_replace() -> None:
    """Test custom replacement character."""
    result = remove_low_complexity_regions("AAAAAAA", window_size=4, complexity_threshold=1.0, replace_with='X')
    assert 'X' in result
    assert 'N' not in result


def test_remove_low_complexity_regions_short_sequence() -> None:
    """Test sequence shorter than window size."""
    seq = "ATGC"
    result = remove_low_complexity_regions(seq, window_size=10)
    assert result == seq  # Returned unchanged


def test_remove_low_complexity_regions_window_too_small() -> None:
    """Test ValueError for window size too small."""
    with pytest.raises(ValueError, match="window_size must be at least 2"):
        remove_low_complexity_regions("ATGC", window_size=1)


def test_remove_low_complexity_regions_invalid_threshold() -> None:
    """Test ValueError for invalid complexity threshold."""
    with pytest.raises(ValueError, match="complexity_threshold must be between 0 and 2"):
        remove_low_complexity_regions("ATGC", complexity_threshold=3.0)


def test_remove_low_complexity_regions_invalid_replace() -> None:
    """Test ValueError for multi-character replacement."""
    with pytest.raises(ValueError, match="replace_with must be a single character"):
        remove_low_complexity_regions("ATGC", replace_with="NN")


def test_remove_low_complexity_regions_type_error() -> None:
    """Test TypeError for non-string seq."""
    with pytest.raises(TypeError, match="seq must be a string"):
        remove_low_complexity_regions(123)
