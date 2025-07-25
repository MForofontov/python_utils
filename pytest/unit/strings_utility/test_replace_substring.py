import pytest
from strings_utility.replace_substring import replace_substring


def test_replace_substring_basic() -> None:
    """
    Test the replace_substring function with a basic string and substrings.
    """
    # Test case 1: Basic string and substrings
    assert (
        replace_substring("hello world", "world", "earth") == "hello earth"
    ), "Failed on basic string and substrings"


def test_replace_substring_no_occurrence() -> None:
    """
    Test the replace_substring function with a string that does not contain the old substring.
    """
    # Test case 2: No occurrence of the old substring
    assert (
        replace_substring("hello world", "there", "earth") == "hello world"
    ), "Failed on no occurrence of the old substring"


def test_replace_substring_empty_string() -> None:
    """
    Test the replace_substring function with an empty string.
    """
    # Test case 3: Empty string
    assert replace_substring("", "hello", "hi") == "", "Failed on empty string"


def test_replace_substring_empty_old() -> None:
    """
    Test the replace_substring function with an empty old substring.
    """
    # Test case 4: Empty old substring
    assert (
        replace_substring("hello", "", "hi") == "hello"
    ), "Failed on empty old substring"


def test_replace_substring_empty_new() -> None:
    """
    Test the replace_substring function with an empty new substring.
    """
    # Test case 5: Empty new substring
    assert (
        replace_substring("hello world", "world", "") == "hello "
    ), "Failed on empty new substring"


def test_replace_substring_special_characters() -> None:
    """
    Test the replace_substring function with a string that contains special characters.
    """
    # Test case 6: String with special characters
    assert (
        replace_substring("hello!@# world", "!@#", "!!!") == "hello!!! world"
    ), "Failed on string with special characters"


def test_replace_substring_mixed_case() -> None:
    """
    Test the replace_substring function with a string that contains mixed case letters.
    """
    # Test case 7: String with mixed case letters
    assert (
        replace_substring("HeLLo WoRLd", "WoRLd", "earth") == "HeLLo earth"
    ), "Failed on string with mixed case letters"


def test_replace_substring_non_english_characters() -> None:
    """
    Test the replace_substring function with a string that contains non-English characters.
    """
    # Test case 8: String with non-English characters
    assert (
        replace_substring("héllo wörld", "wörld", "earth") == "héllo earth"
    ), "Failed on string with non-English characters"


def test_replace_substring_mixed_whitespace() -> None:
    """
    Test the replace_substring function with a string that contains mixed whitespace characters.
    """
    # Test case 9: String with mixed whitespace characters
    assert (
        replace_substring("hello \t\nworld", "\t\n", " ") == "hello  world"
    ), "Failed on string with mixed whitespace characters"


def test_replace_substring_invalid_string_type() -> None:
    """
    Test the replace_substring function with an invalid string type.
    """
    # Test case 10: Invalid string type
    with pytest.raises(TypeError):
        replace_substring(12345, "hello", "hi")


def test_replace_substring_invalid_old_type() -> None:
    """
    Test the replace_substring function with an invalid old substring type.
    """
    # Test case 11: Invalid old substring type
    with pytest.raises(TypeError):
        replace_substring("hello world", 123, "hi")


def test_replace_substring_invalid_new_type() -> None:
    """
    Test the replace_substring function with an invalid new substring type.
    """
    # Test case 12: Invalid new substring type
    with pytest.raises(TypeError):
        replace_substring("hello world", "world", 123)
