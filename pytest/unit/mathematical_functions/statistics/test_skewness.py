import pytest
import math
from mathematical_functions.statistics.skewness import skewness


def test_skewness_symmetric_distribution() -> None:
    """
    Test case 1: Test skewness of symmetric distribution (should be close to 0).
    """
    values = [1, 2, 3, 4, 5]
    result = skewness(values)
    assert abs(result) < 1e-10  # Should be very close to 0


def test_skewness_positive_skew() -> None:
    """
    Test case 2: Test skewness with positive skew (tail to the right).
    """
    values = [1, 1, 1, 2, 3, 4, 5]  # More values on left, tail to right
    result = skewness(values)
    assert result > 0


def test_skewness_negative_skew() -> None:
    """
    Test case 3: Test skewness with negative skew (tail to the left).
    """
    values = [1, 2, 3, 4, 5, 5, 5]  # More values on right, tail to left
    result = skewness(values)
    assert result < 0


def test_skewness_larger_dataset() -> None:
    """
    Test case 4: Test skewness with larger dataset.
    """
    # Create a right-skewed distribution
    values = [1]*10 + [2]*8 + [3]*6 + [4]*4 + [5]*2 + [10]*1
    result = skewness(values)
    assert result > 0  # Should be positively skewed


def test_skewness_normal_like_distribution() -> None:
    """
    Test case 5: Test skewness with normal-like distribution.
    """
    values = [1, 2, 2, 3, 3, 3, 4, 4, 5]  # Bell curve-like
    result = skewness(values)
    assert abs(result) < 1.0  # Should be close to 0 but not exactly


def test_skewness_floats() -> None:
    """
    Test case 6: Test skewness with floating-point numbers.
    """
    values = [1.1, 2.2, 3.3, 4.4, 5.5]
    result = skewness(values)
    assert abs(result) < 1e-10  # Symmetric, should be close to 0


def test_skewness_negative_values() -> None:
    """
    Test case 7: Test skewness with negative values.
    """
    values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    result = skewness(values)
    assert abs(result) < 0.1  # Should be close to 0 (symmetric)


def test_skewness_extreme_outlier() -> None:
    """
    Test case 8: Test skewness with extreme outlier.
    """
    values = [1, 2, 3, 4, 5, 100]  # Extreme positive outlier
    result = skewness(values)
    assert result > 1.0  # Should be highly positively skewed


def test_skewness_minimum_data_points() -> None:
    """
    Test case 9: Test skewness with exactly 3 data points.
    """
    values = [1, 2, 3]
    result = skewness(values)
    assert isinstance(result, float)  # Should work with 3 points


def test_skewness_empty_list() -> None:
    """
    Test case 10: Test skewness with empty list.
    """
    with pytest.raises(ValueError, match="skewness requires at least 3 values"):
        skewness([])


def test_skewness_insufficient_data() -> None:
    """
    Test case 11: Test skewness with insufficient data points.
    """
    with pytest.raises(ValueError, match="skewness requires at least 3 values"):
        skewness([1, 2])


def test_skewness_identical_values() -> None:
    """
    Test case 12: Test skewness with all identical values.
    """
    values = [5, 5, 5, 5, 5]
    with pytest.raises(ValueError, match="all values are identical, cannot calculate skewness"):
        skewness(values)


def test_skewness_type_error_not_list() -> None:
    """
    Test case 13: Test skewness with invalid type for values.
    """
    with pytest.raises(TypeError, match="values must be a list"):
        skewness("not a list")


def test_skewness_type_error_non_numeric() -> None:
    """
    Test case 14: Test skewness with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        skewness([1, 2, "three", 4, 5])


def test_skewness_mixed_data_types() -> None:
    """
    Test case 15: Test skewness with mixed int and float values.
    """
    values = [1, 2.5, 3, 4.5, 5]
    result = skewness(values)
    assert isinstance(result, float)
    assert abs(result) < 1e-10  # Should be close to 0 (symmetric)
