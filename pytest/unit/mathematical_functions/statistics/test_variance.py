import pytest
from mathematical_functions.statistics.variance import variance


def test_variance_sample() -> None:
    """
    Test case 1: Test variance function with sample variance.
    """
    values = [1, 2, 3, 4, 5]
    result = variance(values, sample=True)
    # Expected sample variance for [1,2,3,4,5] is 2.5
    assert abs(result - 2.5) < 1e-10


def test_variance_population() -> None:
    """
    Test case 2: Test variance function with population variance.
    """
    values = [1, 2, 3, 4, 5]
    result = variance(values, sample=False)
    # Expected population variance for [1,2,3,4,5] is 2.0
    assert abs(result - 2.0) < 1e-10


def test_variance_zero_variance() -> None:
    """
    Test case 3: Test variance function with identical values.
    """
    values = [5, 5, 5, 5]
    result = variance(values)
    assert result == 0.0


def test_variance_floats() -> None:
    """
    Test case 4: Test variance function with floating-point numbers.
    """
    values = [1.5, 2.5, 3.5, 4.5]
    result = variance(values, sample=True)
    # Expected sample variance ≈ 1.6667
    assert abs(result - (5.0/3.0)) < 1e-10


def test_variance_two_values() -> None:
    """
    Test case 5: Test variance function with two values.
    """
    values = [1, 3]
    result = variance(values, sample=True)
    # Sample variance of [1, 3] is 2.0
    assert abs(result - 2.0) < 1e-10


def test_variance_negative_values() -> None:
    """
    Test case 6: Test variance function with negative values.
    """
    values = [-2, -1, 0, 1, 2]
    result = variance(values, sample=True)
    # Expected sample variance ≈ 2.5
    assert abs(result - 2.5) < 1e-10


def test_variance_empty_list() -> None:
    """
    Test case 7: Test variance function with empty list.
    """
    with pytest.raises(ValueError, match="values cannot be empty"):
        variance([])


def test_variance_single_value_sample() -> None:
    """
    Test case 8: Test variance function with single value and sample=True.
    """
    with pytest.raises(ValueError, match="sample variance requires at least 2 values"):
        variance([42], sample=True)


def test_variance_single_value_population() -> None:
    """
    Test case 9: Test variance function with single value and sample=False.
    """
    values = [42]
    result = variance(values, sample=False)
    assert result == 0.0


def test_variance_type_error_not_list() -> None:
    """
    Test case 10: Test variance function with invalid type for values.
    """
    with pytest.raises(TypeError, match="values must be a list"):
        variance("not a list")


def test_variance_type_error_non_numeric() -> None:
    """
    Test case 11: Test variance function with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        variance([1, 2, "three", 4])


def test_variance_type_error_sample_not_bool() -> None:
    """
    Test case 12: Test variance function with invalid type for sample parameter.
    """
    with pytest.raises(TypeError, match="sample must be a boolean"):
        variance([1, 2, 3], sample="true")
