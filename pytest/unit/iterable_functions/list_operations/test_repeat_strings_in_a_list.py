import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from pyutils_collection.iterable_functions.list_operations.repeat_strings_in_a_list import (
    repeat_strings_in_a_list,
)


def test_repeat_strings_in_a_list_success() -> None:
    """
    Test case 1: Test the repeat_strings_in_a_list function with valid inputs.
    """
    string = "a"
    times = 3
    expected_output = ["a", "a", "a"]
    assert repeat_strings_in_a_list(string, times) == expected_output


def test_repeat_strings_in_a_list_zero_times() -> None:
    """
    Test case 2: Test the repeat_strings_in_a_list function with zero times.
    """
    string: str = "a"
    times: int = 0
    expected_output: list[str] = []
    assert repeat_strings_in_a_list(string, times) == expected_output


def test_repeat_strings_in_a_list_empty_string() -> None:
    """
    Test case 3: Test the repeat_strings_in_a_list function with an empty string.
    """
    string: str = ""
    times: int = 3
    expected_output: list[str] = ["", "", ""]
    assert repeat_strings_in_a_list(string, times) == expected_output


def test_repeat_strings_in_a_list_type_error_string() -> None:
    """
    Test case 4: Test the repeat_strings_in_a_list function with invalid type for string.
    """
    with pytest.raises(TypeError):
        repeat_strings_in_a_list(123, 3)


def test_repeat_strings_in_a_list_type_error_times() -> None:
    """
    Test case 5: Test the repeat_strings_in_a_list function with invalid type for times.
    """
    with pytest.raises(TypeError):
        repeat_strings_in_a_list("a", "3")


def test_repeat_strings_in_a_list_value_error_times() -> None:
    """
    Test case 6: Test the repeat_strings_in_a_list function with negative times.
    """
    with pytest.raises(ValueError):
        repeat_strings_in_a_list("a", -1)
