import pytest
from strings_utility.find_substring import find_substring


def test_substring_present() -> None:
    """
    Test case 1: Test the find_substring function when the substring is present in the string.
    """
    assert find_substring("hello world", "world") == 6, "Failed on substring present"


def test_substring_not_present() -> None:
    """
    Test case 2: Test the find_substring function when the substring is not present in the string.
    """
    assert (
        find_substring("hello world", "there") == -1
    ), "Failed on substring not present"


def test_substring_entire_string() -> None:
    """
    Test case 3: Test the find_substring function when the substring is the entire string.
    """
    assert (
        find_substring("hello", "hello") == 0
    ), "Failed on substring is the entire string"


def test_empty_substring() -> None:
    """
    Test case 4: Test the find_substring function when the substring is an empty string.
    """
    assert find_substring("hello", "") == 0, "Failed on empty substring"


def test_empty_string() -> None:
    """
    Test case 5: Test the find_substring function when the string is empty.
    """
    assert find_substring("", "hello") == -1, "Failed on empty string"


def test_both_empty() -> None:
    """
    Test case 6: Test the find_substring function when both the string and the substring are empty.
    """
    assert find_substring("", "") == 0, "Failed on both string and substring empty"


def test_substring_beginning() -> None:
    """
    Test case 7: Test the find_substring function when the substring is at the beginning of the string.
    """
    assert (
        find_substring("hello world", "hello") == 0
    ), "Failed on substring at the beginning"


def test_substring_end() -> None:
    """
    Test case 8: Test the find_substring function when the substring is at the end of the string.
    """
    assert find_substring("hello world", "world") == 6, "Failed on substring at the end"


def test_substring_middle() -> None:
    """
    Test case 9: Test the find_substring function when the substring is in the middle of the string.
    """
    assert (
        find_substring("hello world", "lo wo") == 3
    ), "Failed on substring in the middle"


def test_single_character_present() -> None:
    """
    Test case 10: Test the find_substring function when the substring is a single character present in the string.
    """
    assert find_substring("hello world", "o") == 4, "Failed on single character present"


def test_single_character_not_present() -> None:
    """
    Test case 11: Test the find_substring function when the substring is a single character not present in the string.
    """
    assert (
        find_substring("hello world", "x") == -1
    ), "Failed on single character not present"


def test_special_characters() -> None:
    """
    Test case 12: Test the find_substring function when the substring contains special characters.
    """
    assert (
        find_substring("hello!@# world", "!@#") == 5
    ), "Failed on substring with special characters"


def test_numbers() -> None:
    """
    Test case 13: Test the find_substring function when the substring contains numbers.
    """
    assert (
        find_substring("hello123 world", "123") == 5
    ), "Failed on substring with numbers"


def test_mixed_case() -> None:
    """
    Test case 14: Test the find_substring function when the substring has mixed case.
    """
    assert (
        find_substring("Hello World", "world") == -1
    ), "Failed on mixed case substring"


def test_mixed_case_sensitive() -> None:
    """
    Test case 15: Test the find_substring function when the substring has mixed case (case sensitive).
    """
    assert (
        find_substring("Hello World", "World") == 6
    ), "Failed on mixed case substring (case sensitive)"


def test_spaces() -> None:
    """
    Test case 16: Test the find_substring function when the substring contains spaces.
    """
    assert find_substring("hello world", " ") == 5, "Failed on substring with spaces"


def test_newline_characters() -> None:
    """
    Test case 17: Test the find_substring function when the substring contains newline characters.
    """
    assert (
        find_substring("hello\nworld", "\n") == 5
    ), "Failed on substring with newline characters"


def test_tab_characters() -> None:
    """
    Test case 18: Test the find_substring function when the substring contains tab characters.
    """
    assert (
        find_substring("hello\tworld", "\t") == 5
    ), "Failed on substring with tab characters"


def test_leading_trailing_spaces() -> None:
    """
    Test case 19: Test the find_substring function when the substring contains leading and trailing spaces.
    """
    assert (
        find_substring("  hello world  ", "hello") == 2
    ), "Failed on substring with leading and trailing spaces"


def test_punctuation() -> None:
    """
    Test case 20: Test the find_substring function when the substring contains punctuation.
    """
    assert (
        find_substring("hello, world!", "world!") == 7
    ), "Failed on substring with punctuation"


def test_non_english_characters() -> None:
    """
    Test case 21: Test the find_substring function when the substring contains non-English characters.
    """
    assert (
        find_substring("héllo wörld", "wörld") == 6
    ), "Failed on substring with non-English characters"


def test_find_substring_invalid_string_type() -> None:
    """
    Test case 22: Test the find_substring function with an invalid string type.
    """
    with pytest.raises(TypeError):
        find_substring(12345, "hello")


def test_find_substring_invalid_substring_type() -> None:
    """
    Test case 23: Test the find_substring function with an invalid substring type.
    """
    with pytest.raises(TypeError):
        find_substring("hello world", 123)
