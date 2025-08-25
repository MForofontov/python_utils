import pytest
from statistics_functions.mode import mode


def test_mode_single_mode() -> None:
    """
    Test case 1: Test the mode function with a single mode.
    """
    values: list[int] = [1, 2, 2, 3, 4]
    expected_output: int = 2
    assert mode(values) == expected_output


def test_mode_multiple_modes() -> None:
    """
    Test case 2: Test the mode function with multiple modes.
    """
    values: list[int] = [1, 1, 2, 2, 3]
    expected_output: list[int] = [1, 2]
    assert mode(values) == expected_output


def test_mode_all_same_frequency() -> None:
    """
    Test case 3: Test the mode function when all values have same frequency.
    """
    values: list[int] = [1, 2, 3]
    expected_output: list[int] = [1, 2, 3]
    assert mode(values) == expected_output


def test_mode_strings() -> None:
    """
    Test case 4: Test the mode function with strings.
    """
    values: list[str] = ['a', 'b', 'b', 'c']
    expected_output: str = 'b'
    assert mode(values) == expected_output


def test_mode_mixed_types() -> None:
    """
    Test case 5: Test the mode function with mixed types.
    """
    values: list = [1, 1, 'a', 'a', 2]
    result = mode(values)
    # Should return list with 1 and 'a' (both appear twice)
    assert isinstance(result, list)
    assert len(result) == 2
    assert 1 in result and 'a' in result


def test_mode_single_value() -> None:
    """
    Test case 6: Test the mode function with a single value.
    """
    values: list[int] = [42]
    expected_output: int = 42
    assert mode(values) == expected_output


def test_mode_floats() -> None:
    """
    Test case 7: Test the mode function with floating-point numbers.
    """
    values: list[float] = [1.1, 2.2, 2.2, 3.3]
    expected_output: float = 2.2
    assert mode(values) == expected_output


def test_mode_multiple_string_modes() -> None:
    """
    Test case 8: Test the mode function with multiple string modes.
    """
    values: list[str] = ['apple', 'banana', 'apple', 'banana', 'cherry']
    result = mode(values)
    expected_output: list[str] = ['apple', 'banana']
    assert result == expected_output


def test_mode_empty_list() -> None:
    """
    Test case 9: Test the mode function with an empty list.
    """
    with pytest.raises(ValueError, match="values cannot be empty"):
        mode([])


def test_mode_type_error_not_list() -> None:
    """
    Test case 10: Test the mode function with invalid type for values.
    """
    with pytest.raises(TypeError, match="values must be a list"):
        mode("not a list")
