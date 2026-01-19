import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from strings_utility.remove_by_regex import remove_by_regex


def test_remove_by_regex_success() -> None:
    """
    Test case 1: Test the remove_by_regex function with valid inputs.
    """
    string: str = "I have an apple and a banana."
    pattern: str = r"\bapple\b"
    expected_output: str = "I have an and a banana."
    assert remove_by_regex(string, pattern) == expected_output


def test_remove_by_regex_no_match() -> None:
    """
    Test case 2: Test the remove_by_regex function with no matching pattern.
    """
    string: str = "I have an apple and a banana."
    pattern: str = r"\bcherry\b"
    expected_output: str = "I have an apple and a banana."
    assert remove_by_regex(string, pattern) == expected_output


def test_remove_by_regex_empty_string() -> None:
    """
    Test case 3: Test the remove_by_regex function with an empty string.
    """
    string: str = ""
    pattern: str = r"\bapple\b"
    expected_output: str = ""
    assert remove_by_regex(string, pattern) == expected_output


def test_remove_by_regex_empty_pattern() -> None:
    """
    Test case 4: Test the remove_by_regex function with an empty pattern.
    """
    string: str = "I have an apple and a banana."
    pattern: str = ""
    expected_output: str = "I have an apple and a banana."
    assert remove_by_regex(string, pattern) == expected_output


def test_remove_by_regex_type_error_string() -> None:
    """
    Test case 5: Test the remove_by_regex function with invalid type for string.
    """
    with pytest.raises(TypeError):
        remove_by_regex(123, r"\bapple\b")


def test_remove_by_regex_type_error_pattern() -> None:
    """
    Test case 6: Test the remove_by_regex function with invalid type for pattern.
    """
    with pytest.raises(TypeError):
        remove_by_regex("I have an apple and a banana.", 123)
