import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from pyutils_collection.strings_utility.create_whitespace_string import create_whitespace_string


def test_create_whitespace_string_success() -> None:
    """
    Test case 1: Test the create_whitespace_string function with a valid input string.
    """
    input_string: str = "hello"
    expected_output: str = "     "
    assert create_whitespace_string(input_string) == expected_output


def test_create_whitespace_string_empty_string() -> None:
    """
    Test case 2: Test the create_whitespace_string function with an empty input string.
    """
    input_string: str = ""
    expected_output: str = ""
    assert create_whitespace_string(input_string) == expected_output


def test_create_whitespace_string_single_character() -> None:
    """
    Test case 3: Test the create_whitespace_string function with a single character input string.
    """
    input_string: str = "a"
    expected_output: str = " "
    assert create_whitespace_string(input_string) == expected_output


def test_create_whitespace_string_whitespace_string() -> None:
    """
    Test case 4: Test the create_whitespace_string function with a whitespace input string.
    """
    input_string: str = "   "
    expected_output: str = "   "
    assert create_whitespace_string(input_string) == expected_output


def test_create_whitespace_string_type_error() -> None:
    """
    Test case 5: Test the create_whitespace_string function with invalid type for input_string.
    """
    with pytest.raises(TypeError):
        create_whitespace_string(12345)
