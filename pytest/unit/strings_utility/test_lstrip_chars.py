import pytest
from strings_utility.lstrip_chars import lstrip_chars


def test_lstrip_chars_single_character() -> None:
    """
    Test case 1: Test the lstrip_chars function with a single character to strip.
    """
    assert (
        lstrip_chars("...hello...", ".") == "hello..."
    ), "Failed on single character strip"


def test_lstrip_chars_multiple_characters() -> None:
    """
    Test case 2: Test the lstrip_chars function with multiple characters to strip.
    """
    assert (
        lstrip_chars("xyzhellozyx", "xyz") == "hellozyx"
    ), "Failed on multiple characters strip"


def test_lstrip_chars_no_match() -> None:
    """
    Test case 3: Test the lstrip_chars function when there are no matching characters to strip.
    """
    assert (
        lstrip_chars("hello", "xyz") == "hello"
    ), "Failed on no matching characters to strip"


def test_lstrip_chars_empty_string() -> None:
    """
    Test case 4: Test the lstrip_chars function with an empty string.
    """
    assert lstrip_chars("", "xyz") == "", "Failed on empty string"


def test_lstrip_chars_no_chars_argument() -> None:
    """
    Test case 5: Test the lstrip_chars function with an empty chars argument.
    """
    assert lstrip_chars(
        "hello", "") == "hello", "Failed on empty chars argument"


def test_lstrip_chars_all_match() -> None:
    """
    Test case 6: Test the lstrip_chars function when all characters match the strip characters.
    """
    assert (
        lstrip_chars("aaaa", "a") == ""
    ), "Failed when all characters match strip characters"


def test_lstrip_chars_special_characters() -> None:
    """
    Test case 7: Test the lstrip_chars function with special characters.
    """
    assert (
        lstrip_chars("!!!hello!!!", "!") == "hello!!!"
    ), "Failed on special character strip"


def test_lstrip_chars_leading_and_trailing() -> None:
    """
    Test case 8: Test the lstrip_chars function with both leading and trailing characters to strip.
    """
    assert (
        lstrip_chars("///hello///", "/") == "hello///"
    ), "Failed on leading and trailing characters"


def test_lstrip_chars_numbers_and_letters() -> None:
    """
    Test case 9: Test the lstrip_chars function with a mix of numbers and letters to strip.
    """
    assert (
        lstrip_chars("123abc123", "123") == "abc123"
    ), "Failed on numbers and letters mix"


def test_lstrip_chars_unicode_characters() -> None:
    """
    Test case 10: Test the lstrip_chars function with unicode characters to strip.
    """
    assert (
        lstrip_chars("😊😊hello😊😊", "😊") == "hello😊😊"
    ), "Failed on unicode characters"


def test_lstrip_chars_mixed_whitespace() -> None:
    """
    Test case 11: Test the lstrip_chars function with mixed whitespace to strip.
    """
    assert (
        lstrip_chars("   \thello   ", " \t") == "hello   "
    ), "Failed on mixed whitespace"


def test_lstrip_chars_only_spaces() -> None:
    """
    Test case 12: Test the lstrip_chars function when the input string is only spaces.
    """
    assert lstrip_chars(
        "     ", " ") == "", "Failed on input string with only spaces"


def test_lstrip_chars_only_numbers() -> None:
    """
    Test case 13: Test the lstrip_chars function with a string of only numbers.
    """
    assert (
        lstrip_chars("123456789", "123") == "456789"
    ), "Failed on string of only numbers"


def test_lstrip_chars_partial_match() -> None:
    """
    Test case 14: Test the lstrip_chars function when only part of the string matches.
    """
    assert lstrip_chars("abcdef", "abc") == "def", "Failed on partial match"


def test_lstrip_chars_partial_non_match() -> None:
    """
    Test case 15: Test the lstrip_chars function when chars partially overlap but don't match fully.
    """
    assert lstrip_chars(
        "abccba", "a") == "bccba", "Failed on partial non-match"


def test_lstrip_chars_strip_same_as_string() -> None:
    """
    Test case 16: Test the lstrip_chars function when the chars to strip are the same as the string.
    """
    assert (
        lstrip_chars("xyz", "xyz") == ""
    ), "Failed when chars to strip are the same as string"


def test_lstrip_chars_alphanumeric() -> None:
    """
    Test case 17: Test the lstrip_chars function with a mix of alphanumeric characters to strip.
    """
    assert lstrip_chars(
        "123abc456", "123") == "abc456", "Failed on alphanumeric mix"


def test_lstrip_chars_substring_in_middle() -> None:
    """
    Test case 18: Test the lstrip_chars function when the strip characters appear in the middle of the string.
    """
    assert (
        lstrip_chars("hello123world", "hello") == "123world"
    ), "Failed on substring in middle"


def test_lstrip_chars_case_sensitivity() -> None:
    """
    Test case 19: Test the lstrip_chars function for case sensitivity in chars to strip.
    """
    assert lstrip_chars(
        "aAaHello", "a") == "AaHello", "Failed on case sensitivity"


def test_lstrip_chars_with_escapes() -> None:
    """
    Test case 20: Test the lstrip_chars function when chars include escape characters.
    """
    assert lstrip_chars(
        "\n\tHello", "\n\t") == "Hello", "Failed on escape characters"


def test_lstrip_chars_invalid_string_type() -> None:
    """
    Test case 21: Test the lstrip_chars function with an invalid string type.
    """
    with pytest.raises(TypeError):
        lstrip_chars(12345, "xyz")


def test_lstrip_chars_invalid_chars_type() -> None:
    """
    Test case 22: Test the lstrip_chars function with an invalid chars type.
    """
    with pytest.raises(TypeError):
        lstrip_chars("hello", 123)
