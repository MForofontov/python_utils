import pytest
from iterable_functions.repeat_strings_in_a_list import repeat_strings_in_a_list

def test_repeat_strings_in_a_list_success() -> None:
    """
    Test the repeat_strings_in_a_list function with valid inputs.
    """
    # Test case 1: Valid inputs
    string = "a"
    times = 3
    expected_output = ["a", "a", "a"]
    assert repeat_strings_in_a_list(string, times) == expected_output

def test_repeat_strings_in_a_list_zero_times() -> None:
    """
    Test the repeat_strings_in_a_list function with zero times.
    """
    # Test case 2: Zero times
    string: str = "a"
    times: int = 0
    expected_output: list[str] = []
    assert repeat_strings_in_a_list(string, times) == expected_output

def test_repeat_strings_in_a_list_empty_string() -> None:
    """
    Test the repeat_strings_in_a_list function with an empty string.
    """
    # Test case 3: Empty string
    string: str = ""
    times: int = 3
    expected_output: list[str] = ["", "", ""]
    assert repeat_strings_in_a_list(string, times) == expected_output

def test_repeat_strings_in_a_list_type_error_string() -> None:
    """
    Test the repeat_strings_in_a_list function with invalid type for string.
    """
    # Test case 4: Invalid type for string
    with pytest.raises(TypeError):
        repeat_strings_in_a_list(123, 3)

def test_repeat_strings_in_a_list_type_error_times() -> None:
    """
    Test the repeat_strings_in_a_list function with invalid type for times.
    """
    # Test case 5: Invalid type for times
    with pytest.raises(TypeError):
        repeat_strings_in_a_list("a", "3")

def test_repeat_strings_in_a_list_value_error_times() -> None:
    """
    Test the repeat_strings_in_a_list function with negative times.
    """
    # Test case 6: Negative times
    with pytest.raises(ValueError):
        repeat_strings_in_a_list("a", -1)
