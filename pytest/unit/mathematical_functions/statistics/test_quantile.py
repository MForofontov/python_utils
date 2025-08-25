import pytest
from mathematical_functions.statistics.quantile import quantile


def test_quantile_median() -> None:
    """
    Test case 1: Test quantile function for median (0.5 quantile).
    """
    values = [1, 2, 3, 4, 5]
    result = quantile(values, 0.5)
    assert result == 3.0


def test_quantile_first_quartile() -> None:
    """
    Test case 2: Test quantile function for first quartile (0.25 quantile).
    """
    values = [1, 2, 3, 4, 5]
    result = quantile(values, 0.25)
    assert result == 2.0


def test_quantile_third_quartile() -> None:
    """
    Test case 3: Test quantile function for third quartile (0.75 quantile).
    """
    values = [1, 2, 3, 4, 5]
    result = quantile(values, 0.75)
    assert result == 4.0


def test_quantile_minimum() -> None:
    """
    Test case 4: Test quantile function for minimum (0.0 quantile).
    """
    values = [1, 2, 3, 4, 5]
    result = quantile(values, 0.0)
    assert result == 1.0


def test_quantile_maximum() -> None:
    """
    Test case 5: Test quantile function for maximum (1.0 quantile).
    """
    values = [1, 2, 3, 4, 5]
    result = quantile(values, 1.0)
    assert result == 5.0


def test_quantile_even_length() -> None:
    """
    Test case 6: Test quantile function with even-length list.
    """
    values = [1, 2, 3, 4]
    result = quantile(values, 0.5)
    assert result == 2.5


def test_quantile_unsorted() -> None:
    """
    Test case 7: Test quantile function with unsorted values.
    """
    values = [5, 1, 3, 2, 4]
    result = quantile(values, 0.5)
    assert result == 3.0


def test_quantile_floats() -> None:
    """
    Test case 8: Test quantile function with floating-point numbers.
    """
    values = [1.1, 2.2, 3.3, 4.4, 5.5]
    result = quantile(values, 0.5)
    assert result == 3.3


def test_quantile_duplicates() -> None:
    """
    Test case 9: Test quantile function with duplicate values.
    """
    values = [1, 2, 2, 2, 3]
    result = quantile(values, 0.5)
    assert result == 2.0


def test_quantile_interpolation() -> None:
    """
    Test case 10: Test quantile function with interpolation between values.
    """
    values = [1, 2, 3, 4, 5, 6]
    result = quantile(values, 0.35)  # Should interpolate between values
    assert isinstance(result, float)
    assert 2.0 <= result <= 4.0


def test_quantile_empty_list() -> None:
    """
    Test case 11: Test quantile function with empty list.
    """
    with pytest.raises(ValueError, match="values cannot be empty"):
        quantile([], 0.5)


def test_quantile_invalid_q_negative() -> None:
    """
    Test case 12: Test quantile function with invalid q (negative).
    """
    values = [1, 2, 3, 4, 5]
    with pytest.raises(ValueError, match="q must be between 0 and 1"):
        quantile(values, -0.1)


def test_quantile_invalid_q_greater_than_one() -> None:
    """
    Test case 13: Test quantile function with invalid q (> 1).
    """
    values = [1, 2, 3, 4, 5]
    with pytest.raises(ValueError, match="q must be between 0 and 1"):
        quantile(values, 1.5)


def test_quantile_type_error_not_list() -> None:
    """
    Test case 14: Test quantile function with invalid type for values.
    """
    with pytest.raises(TypeError, match="values must be a list"):
        quantile("not a list", 0.5)


def test_quantile_type_error_q_not_numeric() -> None:
    """
    Test case 15: Test quantile function with invalid type for q.
    """
    values = [1, 2, 3, 4, 5]
    with pytest.raises(TypeError, match="q must be numeric"):
        quantile(values, "0.5")


def test_quantile_type_error_non_numeric_values() -> None:
    """
    Test case 16: Test quantile function with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        quantile([1, 2, "three", 4], 0.5)
