import pytest
from mathematical_functions.statistics.correlation_coefficient import correlation_coefficient


def test_correlation_coefficient_perfect_positive() -> None:
    """
    Test case 1: Test correlation coefficient with perfect positive correlation.
    """
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]  # y = 2x
    
    result = correlation_coefficient(x, y)
    assert abs(result - 1.0) < 1e-10


def test_correlation_coefficient_perfect_negative() -> None:
    """
    Test case 2: Test correlation coefficient with perfect negative correlation.
    """
    x = [1, 2, 3, 4, 5]
    y = [5, 4, 3, 2, 1]  # y = 6 - x
    
    result = correlation_coefficient(x, y)
    assert abs(result - (-1.0)) < 1e-10


def test_correlation_coefficient_no_correlation() -> None:
    """
    Test case 3: Test correlation coefficient with no correlation.
    """
    x = [1, 2, 3, 4, 5]
    y = [3, 3, 3, 3, 3]  # constant y
    
    result = correlation_coefficient(x, y)
    # Should be 0 (or undefined, we return 0)
    assert abs(result - 0.0) < 1e-10


def test_correlation_coefficient_partial_correlation() -> None:
    """
    Test case 4: Test correlation coefficient with partial correlation.
    """
    x = [1, 2, 3, 4, 5, 6]
    y = [2, 3, 5, 4, 6, 7]  # roughly increasing but with noise
    
    result = correlation_coefficient(x, y)
    assert 0.5 < result < 1.0  # Should be positive but not perfect


def test_correlation_coefficient_negative_values() -> None:
    """
    Test case 5: Test correlation coefficient with negative values.
    """
    x = [-2, -1, 0, 1, 2]
    y = [-4, -2, 0, 2, 4]  # y = 2x
    
    result = correlation_coefficient(x, y)
    assert abs(result - 1.0) < 1e-10


def test_correlation_coefficient_mixed_signs() -> None:
    """
    Test case 6: Test correlation coefficient with mixed positive/negative values.
    """
    x = [-2, -1, 0, 1, 2]
    y = [4, 2, 0, -2, -4]  # y = -2x
    
    result = correlation_coefficient(x, y)
    assert abs(result - (-1.0)) < 1e-10


def test_correlation_coefficient_floats() -> None:
    """
    Test case 7: Test correlation coefficient with floating point values.
    """
    x = [1.1, 2.2, 3.3, 4.4, 5.5]
    y = [2.2, 4.4, 6.6, 8.8, 11.0]  # y = 2x
    
    result = correlation_coefficient(x, y)
    assert abs(result - 1.0) < 1e-10


def test_correlation_coefficient_empty_lists() -> None:
    """
    Test case 8: Test correlation coefficient with empty lists.
    """
    with pytest.raises(ValueError, match="Input lists cannot be empty"):
        correlation_coefficient([], [])


def test_correlation_coefficient_single_value() -> None:
    """
    Test case 9: Test correlation coefficient with single value.
    """
    with pytest.raises(ValueError, match="Need at least 2 data points"):
        correlation_coefficient([1], [2])


def test_correlation_coefficient_mismatched_lengths() -> None:
    """
    Test case 10: Test correlation coefficient with mismatched lengths.
    """
    with pytest.raises(ValueError, match="x_values and y_values must have the same length"):
        correlation_coefficient([1, 2, 3], [1, 2])


def test_correlation_coefficient_type_errors() -> None:
    """
    Test case 11: Test correlation coefficient with invalid types.
    """
    with pytest.raises(TypeError, match="x_values must be a list"):
        correlation_coefficient("invalid", [1, 2, 3])
    
    with pytest.raises(TypeError, match="y_values must be a list"):
        correlation_coefficient([1, 2, 3], "invalid")


def test_correlation_coefficient_non_numeric() -> None:
    """
    Test case 12: Test correlation coefficient with non-numeric values.
    """
    with pytest.raises(TypeError, match="All values in x_values must be numeric"):
        correlation_coefficient([1, "2", 3], [1, 2, 3])
    
    with pytest.raises(TypeError, match="All values in y_values must be numeric"):
        correlation_coefficient([1, 2, 3], [1, "2", 3])
