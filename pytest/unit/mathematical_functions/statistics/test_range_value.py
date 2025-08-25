import pytest
import math
from mathematical_functions.statistics.range_value import range_value


def test_range_value_basic() -> None:
    """
    Test case 1: Test range calculation with basic values.
    """
    values = [1, 2, 3, 4, 5]
    result = range_value(values)
    assert result == 4  # 5 - 1


def test_range_value_negative_values() -> None:
    """
    Test case 2: Test range calculation with negative values.
    """
    values = [-5, -3, -1, 0, 2, 4]
    result = range_value(values)
    assert result == 9  # 4 - (-5)


def test_range_value_floating_point() -> None:
    """
    Test case 3: Test range calculation with floating point values.
    """
    values = [1.1, 2.7, 3.3, 4.9, 5.5]
    result = range_value(values)
    assert abs(result - 4.4) < 1e-10  # 5.5 - 1.1


def test_range_value_identical_values() -> None:
    """
    Test case 4: Test range calculation with all identical values.
    """
    values = [7, 7, 7, 7, 7]
    result = range_value(values)
    assert result == 0  # 7 - 7


def test_range_value_single_value() -> None:
    """
    Test case 5: Test range calculation with single value.
    """
    values = [42]
    result = range_value(values)
    assert result == 0  # Single value has range 0


def test_range_value_two_values() -> None:
    """
    Test case 6: Test range calculation with two values.
    """
    values = [10, 15]
    result = range_value(values)
    assert result == 5  # 15 - 10


def test_range_value_unordered() -> None:
    """
    Test case 7: Test range calculation with unordered values.
    """
    values = [5, 1, 9, 3, 7, 2, 8]
    result = range_value(values)
    assert result == 8  # 9 - 1


def test_range_value_large_numbers() -> None:
    """
    Test case 8: Test range calculation with large numbers.
    """
    values = [1000000, 2000000, 3000000]
    result = range_value(values)
    assert result == 2000000  # 3000000 - 1000000


def test_range_value_decimal_precision() -> None:
    """
    Test case 9: Test range calculation with high precision decimals.
    """
    values = [1.123456, 2.234567, 3.345678]
    result = range_value(values)
    expected = 3.345678 - 1.123456
    assert abs(result - expected) < 1e-10


def test_range_value_mixed_positive_negative() -> None:
    """
    Test case 10: Test range calculation with mixed positive and negative values.
    """
    values = [-10, -5, 0, 5, 10]
    result = range_value(values)
    assert result == 20  # 10 - (-10)


def test_range_value_very_small_numbers() -> None:
    """
    Test case 11: Test range calculation with very small numbers.
    """
    values = [0.0001, 0.0002, 0.0003]
    result = range_value(values)
    assert abs(result - 0.0002) < 1e-10  # 0.0003 - 0.0001


def test_range_value_empty_list() -> None:
    """
    Test case 12: Test range calculation with empty list.
    """
    with pytest.raises(ValueError, match="range calculation requires at least 1 value"):
        range_value([])


def test_range_value_type_error_not_list() -> None:
    """
    Test case 13: Test range calculation with invalid type for values.
    """
    with pytest.raises(TypeError, match="values must be a list"):
        range_value("not a list")


def test_range_value_type_error_non_numeric() -> None:
    """
    Test case 14: Test range calculation with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        range_value([1, 2, "three", 4, 5])
