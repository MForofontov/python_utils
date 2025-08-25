import pytest
from mathematical_functions.statistics.median import median


def test_median_odd_length() -> None:
    """
    Test case 1: Test the median function with odd-length list.
    """
    values: list[int] = [1, 2, 3, 4, 5]
    expected_output: float = 3.0
    assert median(values) == expected_output


def test_median_even_length() -> None:
    """
    Test case 2: Test the median function with even-length list.
    """
    values: list[int] = [1, 2, 3, 4]
    expected_output: float = 2.5
    assert median(values) == expected_output


def test_median_unsorted() -> None:
    """
    Test case 3: Test the median function with unsorted values.
    """
    values: list[int] = [5, 1, 3, 2, 4]
    expected_output: float = 3.0
    assert median(values) == expected_output


def test_median_floats() -> None:
    """
    Test case 4: Test the median function with floating-point numbers.
    """
    values: list[float] = [1.1, 2.2, 3.3, 4.4, 5.5]
    expected_output: float = 3.3
    assert median(values) == expected_output


def test_median_single_value() -> None:
    """
    Test case 5: Test the median function with a single value.
    """
    values: list[int] = [42]
    expected_output: float = 42.0
    assert median(values) == expected_output


def test_median_duplicates() -> None:
    """
    Test case 6: Test the median function with duplicate values.
    """
    values: list[int] = [1, 2, 2, 2, 3]
    expected_output: float = 2.0
    assert median(values) == expected_output


def test_median_negative_values() -> None:
    """
    Test case 7: Test the median function with negative values.
    """
    values: list[int] = [-5, -1, 0, 1, 5]
    expected_output: float = 0.0
    assert median(values) == expected_output


def test_median_empty_list() -> None:
    """
    Test case 8: Test the median function with an empty list.
    """
    with pytest.raises(ValueError, match="values cannot be empty"):
        median([])


def test_median_type_error_not_list() -> None:
    """
    Test case 9: Test the median function with invalid type for values.
    """
    with pytest.raises(TypeError, match="values must be a list"):
        median("not a list")


def test_median_type_error_non_numeric() -> None:
    """
    Test case 10: Test the median function with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        median([1, 2, "three", 4])
