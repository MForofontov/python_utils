import pytest
from strings_utility.replace_by_regex import replace_by_regex

def test_replace_by_regex_success() -> None:
    """
    Test the replace_by_regex function with valid inputs.
    """
    # Test case 1: Valid inputs
    string: str = "I have an apple and a banana."
    pattern: str = r"\bapple\b"
    replacement: str = "orange"
    expected_output: str = "I have an orange and a banana."
    assert replace_by_regex(string, pattern, replacement) == expected_output

def test_replace_by_regex_no_match() -> None:
    """
    Test the replace_by_regex function with no matching pattern.
    """
    # Test case 2: No matching pattern
    string: str = "I have an apple and a banana."
    pattern: str = r"\bcherry\b"
    replacement: str = "orange"
    expected_output: str = "I have an apple and a banana."
    assert replace_by_regex(string, pattern, replacement) == expected_output

def test_replace_by_regex_multiple_matches() -> None:
    """
    Test the replace_by_regex function with multiple matches.
    """
    # Test case 3: Multiple matches
    string: str = "apple apple apple"
    pattern: str = r"\bapple\b"
    replacement: str = "orange"
    expected_output: str = "orange orange orange"
    assert replace_by_regex(string, pattern, replacement) == expected_output

def test_replace_by_regex_empty_string() -> None:
    """
    Test the replace_by_regex function with an empty string.
    """
    # Test case 4: Empty string
    string: str = ""
    pattern: str = r"\bapple\b"
    replacement: str = "orange"
    expected_output: str = ""
    assert replace_by_regex(string, pattern, replacement) == expected_output

def test_replace_by_regex_empty_pattern() -> None:
    """
    Test the replace_by_regex function with an empty pattern.
    """
    # Test case 5: Empty pattern
    string: str = "I have an apple and a banana."
    pattern: str = ""
    replacement: str = "orange"
    expected_output: str = "I have an apple and a banana."
    assert replace_by_regex(string, pattern, replacement) == expected_output

def test_replace_by_regex_empty_replacement() -> None:
    """
    Test the replace_by_regex function with an empty replacement.
    """
    # Test case 6: Empty replacement
    string: str = "I have an apple and a banana."
    pattern: str = r"\bapple\b"
    replacement: str = ""
    expected_output: str = "I have an and a banana."
    assert replace_by_regex(string, pattern, replacement) == expected_output

def test_replace_by_regex_type_error_string() -> None:
    """
    Test the replace_by_regex function with invalid type for string.
    """
    # Test case 7: Invalid type for string
    with pytest.raises(TypeError):
        replace_by_regex(123, r"\bapple\b", "orange")

def test_replace_by_regex_type_error_pattern() -> None:
    """
    Test the replace_by_regex function with invalid type for pattern.
    """
    # Test case 8: Invalid type for pattern
    with pytest.raises(TypeError):
        replace_by_regex("I have an apple and a banana.", 123, "orange")

def test_replace_by_regex_type_error_replacement() -> None:
    """
    Test the replace_by_regex function with invalid type for replacement.
    """
    # Test case 9: Invalid type for replacement
    with pytest.raises(TypeError):
        replace_by_regex("I have an apple and a banana.", r"\bapple\b", 123)

