import pytest
from strings_utility.contains_substring import contains_substring


def test_contains_substring_present() -> None:
    """
    Test case 1: Test the contains_substring function when the substring is present in the string.
    """
    assert contains_substring("hello world", "world"), "Failed on substring present"


def test_contains_substring_not_present() -> None:
    """
    Test case 2: Test the contains_substring function when the substring is not present in the string.
    """
    assert not contains_substring(
        "hello world", "there"
    ), "Failed on substring not present"


def test_contains_substring_entire_string() -> None:
    """
    Test case 3: Test the contains_substring function when the substring is the entire string.
    """
    assert contains_substring(
        "hello", "hello"
    ), "Failed on substring is the entire string"


def test_contains_substring_empty_substring() -> None:
    """
    Test case 4: Test the contains_substring function when the substring is an empty string.
    """
    assert contains_substring("hello", ""), "Failed on empty substring"


def test_contains_substring_empty_string() -> None:
    """
    Test case 5: Test the contains_substring function when the string is empty.
    """
    assert not contains_substring("", "hello"), "Failed on empty string"


def test_contains_substring_both_empty() -> None:
    """
    Test case 6: Test the contains_substring function when both the string and the substring are empty.
    """
    assert contains_substring("", ""), "Failed on both string and substring empty"


def test_contains_substring_beginning() -> None:
    """
    Test case 7: Test the contains_substring function when the substring is at the beginning of the string.
    """
    assert contains_substring(
        "hello world", "hello"
    ), "Failed on substring at the beginning"


def test_contains_substring_end() -> None:
    """
    Test case 8: Test the contains_substring function when the substring is at the end of the string.
    """
    assert contains_substring("hello world", "world"), "Failed on substring at the end"


def test_contains_substring_middle() -> None:
    """
    Test case 9: Test the contains_substring function when the substring is in the middle of the string.
    """
    assert contains_substring(
        "hello world", "lo wo"
    ), "Failed on substring in the middle"


def test_contains_substring_single_character_present() -> None:
    """
    Test case 10: Test the contains_substring function when the substring is a single character present in the string.
    """
    assert contains_substring("hello world", "o"), "Failed on single character present"


def test_contains_substring_single_character_not_present() -> None:
    """
    Test case 11: Test the contains_substring function when the substring is a single character not present in the string.
    """
    assert not contains_substring(
        "hello world", "x"
    ), "Failed on single character not present"


def test_contains_substring_special_characters() -> None:
    """
    Test case 12: Test the contains_substring function when the substring contains special characters.
    """
    assert contains_substring(
        "hello!@# world", "!@#"
    ), "Failed on substring with special characters"


def test_contains_substring_numbers() -> None:
    """
    Test case 13: Test the contains_substring function when the substring contains numbers.
    """
    assert contains_substring(
        "hello123 world", "123"
    ), "Failed on substring with numbers"


def test_contains_substring_mixed_case() -> None:
    """
    Test case 14: Test the contains_substring function when the substring has mixed case.
    """
    assert not contains_substring(
        "Hello World", "world"
    ), "Failed on mixed case substring"


def test_contains_substring_mixed_case_insensitive() -> None:
    """
    Test case 15: Test the contains_substring function when the substring has mixed case (case insensitive).
    """
    assert contains_substring(
        "Hello World", "World"
    ), "Failed on mixed case substring (case insensitive)"


def test_contains_substring_spaces() -> None:
    """
    Test case 16: Test the contains_substring function when the substring contains spaces.
    """
    assert contains_substring("hello world", " "), "Failed on substring with spaces"


def test_contains_substring_newline_characters() -> None:
    """
    Test case 17: Test the contains_substring function when the substring contains newline characters.
    """
    assert contains_substring(
        "hello\nworld", "\n"
    ), "Failed on substring with newline characters"


def test_contains_substring_tab_characters() -> None:
    """
    Test case 18: Test the contains_substring function when the substring contains tab characters.
    """
    assert contains_substring(
        "hello\tworld", "\t"
    ), "Failed on substring with tab characters"


def test_contains_substring_leading_trailing_spaces() -> None:
    """
    Test case 19: Test the contains_substring function when the substring contains leading and trailing spaces.
    """
    assert contains_substring(
        "  hello world  ", "hello"
    ), "Failed on substring with leading and trailing spaces"


def test_contains_substring_punctuation() -> None:
    """
    Test case 20: Test the contains_substring function when the substring contains punctuation.
    """
    assert contains_substring(
        "hello, world!", "world!"
    ), "Failed on substring with punctuation"


def test_contains_substring_non_english_characters() -> None:
    """
    Test case 21: Test the contains_substring function when the substring contains non-English characters.
    """
    assert contains_substring(
        "héllo wörld", "wörld"
    ), "Failed on substring with non-English characters"


def test_contains_substring_invalid_string_type() -> None:
    """
    Test case 22: Test the contains_substring function with an invalid string type.
    """
    with pytest.raises(TypeError):
        contains_substring(12345, "hello")


def test_contains_substring_invalid_substring_type() -> None:
    """
    Test case 23: Test the contains_substring function with an invalid substring type.
    """
    with pytest.raises(TypeError):
        contains_substring("hello world", 123)
