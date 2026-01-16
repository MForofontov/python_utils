import pytest
from strings_utility.replace_multiple_substrings import replace_multiple_substrings


def test_replace_single_substring() -> None:
    """
    Test case 1: Test the replace_multiple_substrings function with a single substring replacement.
    """
    assert (
        replace_multiple_substrings("hello world", {"world": "there"}) == "hello there"
    ), "Failed on single substring replacement"


def test_replace_multiple_substrings() -> None:
    """
    Test case 2: Test the replace_multiple_substrings function with multiple substring replacements.
    """
    assert (
        replace_multiple_substrings("hello world", {"hello": "hi", "world": "there"})
        == "hi there"
    ), "Failed on multiple substring replacements"


def test_replace_no_substrings() -> None:
    """
    Test case 3: Test the replace_multiple_substrings function with no substrings to replace.
    """
    assert replace_multiple_substrings("hello world", {}) == "hello world", (
        "Failed on no substrings to replace"
    )


def test_replace_non_existing_substring() -> None:
    """
    Test case 4: Test the replace_multiple_substrings function with a non-existing substring.
    """
    assert (
        replace_multiple_substrings("hello world", {"there": "world"}) == "hello world"
    ), "Failed on non-existing substring"


def test_replace_empty_string() -> None:
    """
    Test case 5: Test the replace_multiple_substrings function with an empty string.
    """
    assert replace_multiple_substrings("", {"hello": "hi"}) == "", (
        "Failed on empty string"
    )


def test_replace_special_characters() -> None:
    """
    Test case 6: Test the replace_multiple_substrings function with special characters.
    """
    assert (
        replace_multiple_substrings("hello!@#", {"!@#": " world"}) == "hello world"
    ), "Failed on special characters"


def test_replace_numbers() -> None:
    """
    Test case 7: Test the replace_multiple_substrings function with numbers.
    """
    assert replace_multiple_substrings("123 456", {"123": "789"}) == "789 456", (
        "Failed on numbers"
    )


def test_replace_mixed_case() -> None:
    """
    Test case 8: Test the replace_multiple_substrings function with mixed case substrings.
    """
    assert (
        replace_multiple_substrings("Hello World", {"Hello": "Hi", "World": "There"})
        == "Hi There"
    ), "Failed on mixed case substrings"


def test_replace_whitespace_characters() -> None:
    """
    Test case 9: Test the replace_multiple_substrings function with whitespace characters.
    """
    assert replace_multiple_substrings("hello world", {" ": "-"}) == "hello-world", (
        "Failed on whitespace characters"
    )


def test_replace_newline_characters() -> None:
    """
    Test case 10: Test the replace_multiple_substrings function with newline characters.
    """
    assert replace_multiple_substrings("hello\nworld", {"\n": " "}) == "hello world", (
        "Failed on newline characters"
    )


def test_replace_tab_characters() -> None:
    """
    Test case 11: Test the replace_multiple_substrings function with tab characters.
    """
    assert replace_multiple_substrings("hello\tworld", {"\t": " "}) == "hello world", (
        "Failed on tab characters"
    )


def test_replace_mixed_whitespace_characters() -> None:
    """
    Test case 12: Test the replace_multiple_substrings function with mixed whitespace characters.
    """
    assert (
        replace_multiple_substrings("hello \t\nworld", {"\t": " ", "\n": " "})
        == "hello   world"
    ), "Failed on mixed whitespace characters"


def test_replace_non_english_characters() -> None:
    """
    Test case 13: Test the replace_multiple_substrings function with non-English characters.
    """
    assert (
        replace_multiple_substrings("héllo wörld", {"héllo": "hi", "wörld": "there"})
        == "hi there"
    ), "Failed on non-English characters"


def test_replace_invalid_replacements_type() -> None:
    """
    Test case 14: Test the replace_multiple_substrings function with an invalid replacements type.
    """
    with pytest.raises(TypeError):
        replace_multiple_substrings("hello world", ["hello", "hi"])


def test_replace_invalid_string_type() -> None:
    """
    Test case 15: Test the replace_multiple_substrings function with an invalid string type.
    """
    with pytest.raises(TypeError):
        replace_multiple_substrings(123, {"hello": "hi"})


def test_replace_invalid_key_value_types() -> None:
    """
    Test case 16: Test TypeError when replacements dict has non-string keys or values.
    """
    # Test non-string key
    with pytest.raises(
        TypeError, match="Both keys and values in replacements must be strings"
    ):
        replace_multiple_substrings("hello", {123: "world"})

    # Test non-string value
    with pytest.raises(
        TypeError, match="Both keys and values in replacements must be strings"
    ):
        replace_multiple_substrings("hello", {"hello": 456})
