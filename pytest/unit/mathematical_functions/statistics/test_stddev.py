import pytest
import math
from statistics_functions.stddev import stddev


def test_stddev_sample() -> None:
    """
    Test case 1: Test the stddev function with sample standard deviation.
    """
    values: list[int] = [1, 2, 3, 4, 5]
    result = stddev(values, sample=True)
    # Expected sample stddev for [1,2,3,4,5] is sqrt(2.5) ≈ 1.5811
    assert abs(result - 1.5811388300841898) < 1e-10


def test_stddev_population() -> None:
    """
    Test case 2: Test the stddev function with population standard deviation.
    """
    values: list[int] = [1, 2, 3, 4, 5]
    result = stddev(values, sample=False)
    # Expected population stddev for [1,2,3,4,5] is sqrt(2) ≈ 1.4142
    assert abs(result - 1.4142135623730951) < 1e-10


def test_stddev_zero_variance() -> None:
    """
    Test case 3: Test the stddev function with identical values.
    """
    values: list[int] = [5, 5, 5, 5]
    result = stddev(values)
    assert result == 0.0


def test_stddev_floats() -> None:
    """
    Test case 4: Test the stddev function with floating-point numbers.
    """
    values: list[float] = [1.5, 2.5, 3.5, 4.5]
    result = stddev(values, sample=True)
    # Expected sample stddev ≈ 1.2909944
    assert abs(result - 1.2909944487358056) < 1e-10


def test_stddev_two_values() -> None:
    """
    Test case 5: Test the stddev function with two values.
    """
    values: list[int] = [1, 3]
    result = stddev(values, sample=True)
    # Sample stddev of [1, 3] is sqrt(2) ≈ 1.4142
    assert abs(result - 1.4142135623730951) < 1e-10


def test_stddev_negative_values() -> None:
    """
    Test case 6: Test the stddev function with negative values.
    """
    values: list[int] = [-2, -1, 0, 1, 2]
    result = stddev(values, sample=True)
    # Expected sample stddev ≈ 1.5811
    assert abs(result - 1.5811388300841898) < 1e-10


def test_stddev_empty_list() -> None:
    """
    Test case 7: Test the stddev function with an empty list.
    """
    with pytest.raises(ValueError, match="values cannot be empty"):
        stddev([])


def test_stddev_single_value_sample() -> None:
    """
    Test case 8: Test the stddev function with single value and sample=True.
    """
    with pytest.raises(ValueError, match="sample standard deviation requires at least 2 values"):
        stddev([42], sample=True)


def test_stddev_single_value_population() -> None:
    """
    Test case 9: Test the stddev function with single value and sample=False.
    """
    values: list[int] = [42]
    result = stddev(values, sample=False)
    assert result == 0.0


def test_stddev_type_error_not_list() -> None:
    """
    Test case 10: Test the stddev function with invalid type for values.
    """
    with pytest.raises(TypeError, match="values must be a list"):
        stddev("not a list")


def test_stddev_type_error_non_numeric() -> None:
    """
    Test case 11: Test the stddev function with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        stddev([1, 2, "three", 4])


def test_stddev_type_error_sample_not_bool() -> None:
    """
    Test case 12: Test the stddev function with invalid type for sample parameter.
    """
    with pytest.raises(TypeError, match="sample must be a boolean"):
        stddev([1, 2, 3], sample="true")
