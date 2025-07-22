import pytest
from strings_utility.count_substring import count_substring

def test_count_substring_multiple_occurrences() -> None:
    """
    Test the count_substring function when the substring occurs multiple times.
    """
    # Test case 1: Substring occurs multiple times
    assert count_substring("hello world", "o") == 2, "Failed on multiple occurrences"

def test_count_substring_beginning() -> None:
    """
    Test the count_substring function when the substring occurs at the beginning.
    """
    # Test case 2: Substring occurs at the beginning
    assert count_substring("ababab", "ab") == 3, "Failed on substring at the beginning"

def test_count_substring_end() -> None:
    """
    Test the count_substring function when the substring occurs at the end.
    """
    # Test case 3: Substring occurs at the end
    assert count_substring("hello", "lo") == 1, "Failed on substring at the end"

def test_count_substring_entire_string() -> None:
    """
    Test the count_substring function when the substring is the entire string.
    """
    # Test case 4: Substring is the entire string
    assert count_substring("hello", "hello") == 1, "Failed on substring is the entire string"

def test_count_substring_not_occur() -> None:
    """
    Test the count_substring function when the substring does not occur.
    """
    # Test case 5: Substring does not occur
    assert count_substring("hello", "world") == 0, "Failed on substring does not occur"

def test_count_substring_empty_substring() -> None:
    """
    Test the count_substring function when the substring is empty.
    """
    # Test case 6: Empty substring
    assert count_substring("hello", "") == 6, "Failed on empty substring"

def test_count_substring_empty_string() -> None:
    """
    Test the count_substring function when the string is empty.
    """
    # Test case 7: Empty string
    assert count_substring("", "hello") == 0, "Failed on empty string"

def test_count_substring_both_empty() -> None:
    """
    Test the count_substring function when both the string and the substring are empty.
    """
    # Test case 8: Both string and substring are empty
    assert count_substring("", "") == 1, "Failed on both string and substring empty"

def test_count_substring_overlapping() -> None:
    """
    Test the count_substring function when the substring occurs with overlapping.
    """
    # Test case 9: Substring occurs with overlapping
    assert count_substring("aaaa", "aa") == 2, "Failed on overlapping occurrences"

def test_count_substring_special_characters() -> None:
    """
    Test the count_substring function when the substring contains special characters.
    """
    # Test case 10: Substring occurs with special characters
    assert count_substring("hello!@#hello", "hello") == 2, "Failed on special characters"

def test_count_substring_mixed_case() -> None:
    """
    Test the count_substring function when the substring has mixed case.
    """
    # Test case 11: Substring occurs with mixed case
    assert count_substring("Hello hello", "hello") == 1, "Failed on mixed case"

def test_count_substring_numbers() -> None:
    """
    Test the count_substring function when the substring contains numbers.
    """
    # Test case 12: Substring occurs with numbers
    assert count_substring("123123123", "123") == 3, "Failed on numbers"

def test_count_substring_spaces() -> None:
    """
    Test the count_substring function when the substring contains spaces.
    """
    # Test case 13: Substring occurs with spaces
    assert count_substring("hello world hello", "hello") == 2, "Failed on spaces"

def test_count_substring_newline_characters() -> None:
    """
    Test the count_substring function when the substring contains newline characters.
    """
    # Test case 14: Substring occurs with newline characters
    assert count_substring("hello\nworld\nhello", "hello") == 2, "Failed on newline characters"

def test_count_substring_tab_characters() -> None:
    """
    Test the count_substring function when the substring contains tab characters.
    """
    # Test case 15: Substring occurs with tab characters
    assert count_substring("hello\tworld\thello", "hello") == 2, "Failed on tab characters"

def test_count_substring_mixed_whitespace_characters() -> None:
    """
    Test the count_substring function when the substring contains mixed whitespace characters.
    """
    # Test case 16: Substring occurs with mixed whitespace characters
    assert count_substring("hello \t\nworld \t\nhello", "hello") == 2, "Failed on mixed whitespace characters"

def test_count_substring_leading_trailing_spaces() -> None:
    """
    Test the count_substring function when the substring contains leading and trailing spaces.
    """
    # Test case 17: Substring occurs with leading and trailing spaces
    assert count_substring("  hello world  hello  ", "hello") == 2, "Failed on leading and trailing spaces"

def test_count_substring_punctuation() -> None:
    """
    Test the count_substring function when the substring contains punctuation.
    """
    # Test case 18: Substring occurs with punctuation
    assert count_substring("hello, world! hello.", "hello") == 2, "Failed on punctuation"

def test_count_substring_non_english_characters() -> None:
    """
    Test the count_substring function when the substring contains non-English characters.
    """
    # Test case 19: Substring occurs with non-English characters
    assert count_substring("héllo wörld héllo", "héllo") == 2, "Failed on non-English characters"

def test_count_substring_invalid_string_type() -> None:
    """
    Test the count_substring function with an invalid string type.
    """
    # Test case 20: Invalid string type
    with pytest.raises(TypeError):
        count_substring(12345, "hello")

def test_count_substring_invalid_substring_type() -> None:
    """
    Test the count_substring function with an invalid substring type.
    """
    # Test case 21: Invalid substring type
    with pytest.raises(TypeError):
        count_substring("hello world", 123)


