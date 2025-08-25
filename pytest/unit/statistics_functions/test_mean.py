import pytest
from statistics_functions.mean import mean


def test_mean_success() -> None:
    """
    Test case 1: Test the mean function with valid inputs.
    """
    values: list[int] = [1, 2, 3, 4, 5]
    expected_output: float = 3.0
    assert mean(values) == expected_output


def test_mean_floats() -> None:
    """
    Test case 2: Test the mean function with floating-point numbers.
    """
    values: list[float] = [1.5, 2.5, 3.5, 4.5]
    expected_output: float = 3.0
    assert mean(values) == expected_output


def test_mean_mixed_types() -> None:
    """
    Test case 3: Test the mean function with mixed int and float values.
    """
    values: list[float] = [1, 2.5, 3, 4.5]
    expected_output: float = 2.75
    assert mean(values) == expected_output


def test_mean_single_value() -> None:
    """
    Test case 4: Test the mean function with a single value.
    """
    values: list[int] = [42]
    expected_output: float = 42.0
    assert mean(values) == expected_output


def test_mean_negative_values() -> None:
    """
    Test case 5: Test the mean function with negative values.
    """
    values: list[int] = [-2, -1, 0, 1, 2]
    expected_output: float = 0.0
    assert mean(values) == expected_output


def test_mean_empty_list() -> None:
    """
    Test case 6: Test the mean function with an empty list.
    """
    with pytest.raises(ValueError, match="values cannot be empty"):
        mean([])


def test_mean_type_error_not_list() -> None:
    """
    Test case 7: Test the mean function with invalid type for values.
    """
    with pytest.raises(TypeError, match="values must be a list"):
        mean("not a list")


def test_mean_type_error_non_numeric() -> None:
    """
    Test case 8: Test the mean function with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        mean([1, 2, "three", 4])


def test_mean_type_error_mixed_invalid() -> None:
    """
    Test case 9: Test the mean function with mixed valid and invalid types.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        mean([1, 2.5, None, 4])
