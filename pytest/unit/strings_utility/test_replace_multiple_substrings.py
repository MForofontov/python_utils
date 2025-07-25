import pytest
from strings_utility.replace_multiple_substrings import replace_multiple_substrings


def test_replace_single_substring() -> None:
    """
    Test the replace_multiple_substrings function with a single substring replacement.
    """
    # Test case 1: Single substring replacement
    assert (
        replace_multiple_substrings("hello world", {"world": "there"}) == "hello there"
    ), "Failed on single substring replacement"


def test_replace_multiple_substrings() -> None:
    """
    Test the replace_multiple_substrings function with multiple substring replacements.
    """
    # Test case 2: Multiple substring replacements
    assert (
        replace_multiple_substrings("hello world", {"hello": "hi", "world": "there"})
        == "hi there"
    ), "Failed on multiple substring replacements"


def test_replace_no_substrings() -> None:
    """
    Test the replace_multiple_substrings function with no substrings to replace.
    """
    # Test case 3: No substrings to replace
    assert (
        replace_multiple_substrings("hello world", {}) == "hello world"
    ), "Failed on no substrings to replace"


def test_replace_non_existing_substring() -> None:
    """
    Test the replace_multiple_substrings function with a non-existing substring.
    """
    # Test case 4: Non-existing substring
    assert (
        replace_multiple_substrings("hello world", {"there": "world"}) == "hello world"
    ), "Failed on non-existing substring"


def test_replace_empty_string() -> None:
    """
    Test the replace_multiple_substrings function with an empty string.
    """
    # Test case 5: Empty string
    assert (
        replace_multiple_substrings("", {"hello": "hi"}) == ""
    ), "Failed on empty string"


def test_replace_special_characters() -> None:
    """
    Test the replace_multiple_substrings function with special characters.
    """
    # Test case 6: Special characters
    assert (
        replace_multiple_substrings("hello!@#", {"!@#": " world"}) == "hello world"
    ), "Failed on special characters"


def test_replace_numbers() -> None:
    """
    Test the replace_multiple_substrings function with numbers.
    """
    # Test case 7: Numbers
    assert (
        replace_multiple_substrings("123 456", {"123": "789"}) == "789 456"
    ), "Failed on numbers"


def test_replace_mixed_case() -> None:
    """
    Test the replace_multiple_substrings function with mixed case substrings.
    """
    # Test case 8: Mixed case substrings
    assert (
        replace_multiple_substrings("Hello World", {"Hello": "Hi", "World": "There"})
        == "Hi There"
    ), "Failed on mixed case substrings"


def test_replace_whitespace_characters() -> None:
    """
    Test the replace_multiple_substrings function with whitespace characters.
    """
    # Test case 9: Whitespace characters
    assert (
        replace_multiple_substrings("hello world", {" ": "-"}) == "hello-world"
    ), "Failed on whitespace characters"


def test_replace_newline_characters() -> None:
    """
    Test the replace_multiple_substrings function with newline characters.
    """
    # Test case 10: Newline characters
    assert (
        replace_multiple_substrings("hello\nworld", {"\n": " "}) == "hello world"
    ), "Failed on newline characters"


def test_replace_tab_characters() -> None:
    """
    Test the replace_multiple_substrings function with tab characters.
    """
    # Test case 11: Tab characters
    assert (
        replace_multiple_substrings("hello\tworld", {"\t": " "}) == "hello world"
    ), "Failed on tab characters"


def test_replace_mixed_whitespace_characters() -> None:
    """
    Test the replace_multiple_substrings function with mixed whitespace characters.
    """
    # Test case 12: Mixed whitespace characters
    assert (
        replace_multiple_substrings("hello \t\nworld", {"\t": " ", "\n": " "})
        == "hello   world"
    ), "Failed on mixed whitespace characters"


def test_replace_non_english_characters() -> None:
    """
    Test the replace_multiple_substrings function with non-English characters.
    """
    # Test case 13: Non-English characters
    assert (
        replace_multiple_substrings("héllo wörld", {"héllo": "hi", "wörld": "there"})
        == "hi there"
    ), "Failed on non-English characters"


def test_replace_invalid_replacements_type() -> None:
    """
    Test the replace_multiple_substrings function with an invalid replacements type.
    """
    # Test case 14: Invalid replacements type
    with pytest.raises(TypeError):
        replace_multiple_substrings("hello world", ["hello", "hi"])


def test_replace_invalid_string_type() -> None:
    """
    Test the replace_multiple_substrings function with an invalid string type.
    """
    # Test case 15: Invalid string type
    with pytest.raises(TypeError):
        replace_multiple_substrings(123, {"hello": "hi"})
