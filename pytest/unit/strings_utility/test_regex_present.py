import pytest
from strings_utility.regex_present import regex_present


def test_regex_present_success() -> None:
    """
    Test the regex_present function with valid inputs.
    """
    # Test case 1: Valid inputs
    regex_list: list[str] = [r"\bapple\b", r"\bbanana\b"]
    string: str = "I have an apple and a banana."
    expected_output: bool = True
    assert regex_present(regex_list, string) == expected_output


def test_regex_present_no_match() -> None:
    """
    Test the regex_present function with no matching regex.
    """
    # Test case 2: No matching regex
    regex_list: list[str] = [r"\bapple\b", r"\bbanana\b"]
    string: str = "I have a cherry and a date."
    expected_output: bool = False
    assert regex_present(regex_list, string) == expected_output


def test_regex_present_empty_regex_list() -> None:
    """
    Test the regex_present function with an empty regex list.
    """
    # Test case 3: Empty regex list
    regex_list: list[str] = []
    string: str = "I have an apple and a banana."
    expected_output: bool = False
    assert regex_present(regex_list, string) == expected_output


def test_regex_present_empty_string() -> None:
    """
    Test the regex_present function with an empty string.
    """
    # Test case 4: Empty string
    regex_list: list[str] = [r"\bapple\b", r"\bbanana\b"]
    string: str = ""
    expected_output: bool = False
    assert regex_present(regex_list, string) == expected_output


def test_regex_present_type_error_regex_list() -> None:
    """
    Test the regex_present function with invalid type for regex_list.
    """
    # Test case 5: Invalid type for regex_list
    with pytest.raises(TypeError):
        regex_present("not a list", "I have an apple and a banana.")


def test_regex_present_type_error_elements() -> None:
    """
    Test the regex_present function with invalid elements in regex_list.
    """
    # Test case 6: Invalid elements in regex_list
    with pytest.raises(TypeError):
        regex_present([r"\bapple\b", 123], "I have an apple and a banana.")


def test_regex_present_type_error_string() -> None:
    """
    Test the regex_present function with invalid type for string.
    """
    # Test case 7: Invalid type for string
    with pytest.raises(TypeError):
        regex_present([r"\bapple\b", r"\bbanana\b"], 123)
