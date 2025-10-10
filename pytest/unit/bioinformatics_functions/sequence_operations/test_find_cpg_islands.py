import pytest
from bioinformatics_functions.sequence_operations.find_cpg_islands import (
    find_cpg_islands,
)


def test_find_cpg_islands_high_cpg_content() -> None:
    """
    Test case 1: Finding CpG islands in sequence with high CpG content.
    """
    # Arrange
    seq = "GCGCGCGCGC" * 20  # High CpG content
    window = 50

    # Act
    result = find_cpg_islands(seq, window=window)

    # Assert
    assert len(result) > 0
    assert all(isinstance(island, tuple) for island in result)
    assert all(len(island) == 2 for island in result)


def test_find_cpg_islands_no_islands() -> None:
    """
    Test case 2: Sequence with no CpG islands.
    """
    # Arrange
    seq = "AAATTTTAAAA" * 20  # Low GC content
    window = 50

    # Act
    result = find_cpg_islands(seq, window=window)

    # Assert
    assert result == []


def test_find_cpg_islands_default_parameters() -> None:
    """
    Test case 3: Using default parameters.
    """
    # Arrange
    seq = "GCGCGCGC" * 50  # High CpG, 400 bases

    # Act
    result = find_cpg_islands(seq)

    # Assert
    assert isinstance(result, list)
    assert all(isinstance(island, tuple) for island in result)


def test_find_cpg_islands_custom_window() -> None:
    """
    Test case 4: Custom window size.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    window = 100

    # Act
    result = find_cpg_islands(seq, window=window)

    # Assert
    assert isinstance(result, list)
    if result:
        for start, end in result:
            assert end - start == window


def test_find_cpg_islands_custom_gc_threshold() -> None:
    """
    Test case 5: Custom GC content threshold.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    min_gc = 0.7  # Higher threshold

    # Act
    result = find_cpg_islands(seq, min_gc=min_gc)

    # Assert
    assert isinstance(result, list)


def test_find_cpg_islands_custom_obs_exp() -> None:
    """
    Test case 6: Custom observed/expected ratio.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    min_obs_exp = 0.8  # Higher threshold

    # Act
    result = find_cpg_islands(seq, min_obs_exp=min_obs_exp)

    # Assert
    assert isinstance(result, list)


def test_find_cpg_islands_lowercase_input() -> None:
    """
    Test case 7: Lowercase DNA sequence.
    """
    # Arrange
    seq = "gcgcgcgcgc" * 20
    window = 50

    # Act
    result = find_cpg_islands(seq, window=window)

    # Assert
    assert isinstance(result, list)


def test_find_cpg_islands_short_sequence() -> None:
    """
    Test case 8: Sequence length equal to window.
    """
    # Arrange
    seq = "GCGCGCGC"  # 8 bases
    window = 8

    # Act
    result = find_cpg_islands(seq, window=window)

    # Assert
    assert isinstance(result, list)


def test_find_cpg_islands_type_error_seq_not_string() -> None:
    """
    Test case 9: TypeError when seq is not a string.
    """
    # Arrange
    invalid_seq = 12345  # type: ignore
    expected_message = "seq must be str, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_cpg_islands(invalid_seq)  # type: ignore


def test_find_cpg_islands_type_error_window_not_int() -> None:
    """
    Test case 10: TypeError when window is not an integer.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    invalid_window = "50"  # type: ignore
    expected_message = "window must be int, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_cpg_islands(seq, window=invalid_window)  # type: ignore


def test_find_cpg_islands_type_error_min_gc_not_number() -> None:
    """
    Test case 11: TypeError when min_gc is not a number.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    invalid_min_gc = "0.5"  # type: ignore
    expected_message = "min_gc must be a number, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_cpg_islands(seq, min_gc=invalid_min_gc)  # type: ignore


def test_find_cpg_islands_type_error_min_obs_exp_not_number() -> None:
    """
    Test case 12: TypeError when min_obs_exp is not a number.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    invalid_obs_exp = "0.6"  # type: ignore
    expected_message = "min_obs_exp must be a number, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_cpg_islands(seq, min_obs_exp=invalid_obs_exp)  # type: ignore


def test_find_cpg_islands_value_error_invalid_bases() -> None:
    """
    Test case 13: ValueError for invalid DNA bases.
    """
    # Arrange
    invalid_seq = "GCGCXYZ"
    expected_message = "Sequence contains invalid DNA bases"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_cpg_islands(invalid_seq)


def test_find_cpg_islands_value_error_window_zero() -> None:
    """
    Test case 14: ValueError when window is zero.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    invalid_window = 0
    expected_message = "window must be positive"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_cpg_islands(seq, window=invalid_window)


def test_find_cpg_islands_value_error_window_negative() -> None:
    """
    Test case 15: ValueError when window is negative.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    invalid_window = -10
    expected_message = "window must be positive"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_cpg_islands(seq, window=invalid_window)


def test_find_cpg_islands_value_error_window_too_large() -> None:
    """
    Test case 16: ValueError when window exceeds sequence length.
    """
    # Arrange
    seq = "GCGCGCGC"  # 8 bases
    invalid_window = 100
    expected_message = "window must be positive and <= sequence length"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_cpg_islands(seq, window=invalid_window)


def test_find_cpg_islands_value_error_min_gc_negative() -> None:
    """
    Test case 17: ValueError when min_gc is negative.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    invalid_gc = -0.5
    expected_message = "min_gc must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_cpg_islands(seq, min_gc=invalid_gc)


def test_find_cpg_islands_value_error_min_gc_greater_than_one() -> None:
    """
    Test case 18: ValueError when min_gc is greater than 1.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    invalid_gc = 1.5
    expected_message = "min_gc must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_cpg_islands(seq, min_gc=invalid_gc)


def test_find_cpg_islands_value_error_min_obs_exp_negative() -> None:
    """
    Test case 19: ValueError when min_obs_exp is negative.
    """
    # Arrange
    seq = "GCGCGCGC" * 30
    invalid_obs_exp = -0.5
    expected_message = "min_obs_exp must be non-negative"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_cpg_islands(seq, min_obs_exp=invalid_obs_exp)
