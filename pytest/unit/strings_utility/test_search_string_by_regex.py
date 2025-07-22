import pytest
from strings_utility.search_string_by_regex import search_string_by_regex

def test_search_string_by_regex_success() -> None:
    """
    Test the search_string_by_regex function with valid inputs.
    """
    # Test case 1: Valid inputs
    pattern: str = r"\bapple\b"
    string: str = "I have an apple and a banana."
    expected_output: str = "apple"
    assert search_string_by_regex(pattern, string) == expected_output

def test_search_string_by_regex_no_match() -> None:
    """
    Test the search_string_by_regex function with no matching pattern.
    """
    # Test case 2: No matching pattern
    pattern: str = r"\bcherry\b"
    string: str = "I have an apple and a banana."
    expected_output: None = None
    assert search_string_by_regex(pattern, string) == expected_output

def test_search_string_by_regex_empty_string() -> None:
    """
    Test the search_string_by_regex function with an empty string.
    """
    # Test case 3: Empty string
    pattern: str = r"\bapple\b"
    string: str = ""
    expected_output: None = None
    assert search_string_by_regex(pattern, string) == expected_output

def test_search_string_by_regex_empty_pattern() -> None:
    """
    Test the search_string_by_regex function with an empty pattern.
    """
    # Test case 4: Empty pattern
    pattern: str = ""
    string: str = "I have an apple and a banana."
    expected_output: None = None
    assert search_string_by_regex(pattern, string) == expected_output

def test_search_string_by_regex_type_error_pattern() -> None:
    """
    Test the search_string_by_regex function with invalid type for pattern.
    """
    # Test case 5: Invalid type for pattern
    with pytest.raises(TypeError):
        search_string_by_regex(123, "I have an apple and a banana.")

def test_search_string_by_regex_type_error_string() -> None:
    """
    Test the search_string_by_regex function with invalid type for string.
    """
    # Test case 6: Invalid type for string
    with pytest.raises(TypeError):
        search_string_by_regex(r"\bapple\b", 123)

