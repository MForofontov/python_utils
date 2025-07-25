import pytest
from strings_utility.create_whitespace_string import create_whitespace_string


def test_create_whitespace_string_success() -> None:
    """
    Test the create_whitespace_string function with a valid input string.
    """
    # Test case 1: Valid input string
    input_string: str = "hello"
    expected_output: str = "     "
    assert create_whitespace_string(input_string) == expected_output


def test_create_whitespace_string_empty_string() -> None:
    """
    Test the create_whitespace_string function with an empty input string.
    """
    # Test case 2: Empty input string
    input_string: str = ""
    expected_output: str = ""
    assert create_whitespace_string(input_string) == expected_output


def test_create_whitespace_string_single_character() -> None:
    """
    Test the create_whitespace_string function with a single character input string.
    """
    # Test case 3: Single character input string
    input_string: str = "a"
    expected_output: str = " "
    assert create_whitespace_string(input_string) == expected_output


def test_create_whitespace_string_whitespace_string() -> None:
    """
    Test the create_whitespace_string function with a whitespace input string.
    """
    # Test case 4: Whitespace input string
    input_string: str = "   "
    expected_output: str = "   "
    assert create_whitespace_string(input_string) == expected_output


def test_create_whitespace_string_type_error() -> None:
    """
    Test the create_whitespace_string function with invalid type for input_string.
    """
    # Test case 5: Invalid type for input_string
    with pytest.raises(TypeError):
        create_whitespace_string(12345)
