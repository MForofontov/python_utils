import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from strings_utility.replace_substring import replace_substring


def test_replace_substring_basic() -> None:
    """
    Test case 1: Test the replace_substring function with a basic string and substrings.
    """
    assert replace_substring("hello world", "world", "earth") == "hello earth", (
        "Failed on basic string and substrings"
    )


def test_replace_substring_no_occurrence() -> None:
    """
    Test case 2: Test the replace_substring function with a string that does not contain the old substring.
    """
    assert replace_substring("hello world", "there", "earth") == "hello world", (
        "Failed on no occurrence of the old substring"
    )


def test_replace_substring_empty_string() -> None:
    """
    Test case 3: Test the replace_substring function with an empty string.
    """
    assert replace_substring("", "hello", "hi") == "", "Failed on empty string"


def test_replace_substring_empty_old() -> None:
    """
    Test case 4: Test the replace_substring function with an empty old substring.
    """
    assert replace_substring("hello", "", "hi") == "hello", (
        "Failed on empty old substring"
    )


def test_replace_substring_empty_new() -> None:
    """
    Test case 5: Test the replace_substring function with an empty new substring.
    """
    assert replace_substring("hello world", "world", "") == "hello ", (
        "Failed on empty new substring"
    )


def test_replace_substring_special_characters() -> None:
    """
    Test case 6: Test the replace_substring function with a string that contains special characters.
    """
    assert replace_substring("hello!@# world", "!@#", "!!!") == "hello!!! world", (
        "Failed on string with special characters"
    )


def test_replace_substring_mixed_case() -> None:
    """
    Test case 7: Test the replace_substring function with a string that contains mixed case letters.
    """
    assert replace_substring("HeLLo WoRLd", "WoRLd", "earth") == "HeLLo earth", (
        "Failed on string with mixed case letters"
    )


def test_replace_substring_non_english_characters() -> None:
    """
    Test case 8: Test the replace_substring function with a string that contains non-English characters.
    """
    assert replace_substring("héllo wörld", "wörld", "earth") == "héllo earth", (
        "Failed on string with non-English characters"
    )


def test_replace_substring_mixed_whitespace() -> None:
    """
    Test case 9: Test the replace_substring function with a string that contains mixed whitespace characters.
    """
    assert replace_substring("hello \t\nworld", "\t\n", " ") == "hello  world", (
        "Failed on string with mixed whitespace characters"
    )


def test_replace_substring_invalid_string_type() -> None:
    """
    Test case 10: Test the replace_substring function with an invalid string type.
    """
    with pytest.raises(TypeError):
        replace_substring(12345, "hello", "hi")


def test_replace_substring_invalid_old_type() -> None:
    """
    Test case 11: Test the replace_substring function with an invalid old substring type.
    """
    with pytest.raises(TypeError):
        replace_substring("hello world", 123, "hi")


def test_replace_substring_invalid_new_type() -> None:
    """
    Test case 12: Test the replace_substring function with an invalid new substring type.
    """
    with pytest.raises(TypeError):
        replace_substring("hello world", "world", 123)
