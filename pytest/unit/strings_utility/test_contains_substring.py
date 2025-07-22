import pytest
from strings_utility.contains_substring import contains_substring

def test_contains_substring_present() -> None:
    """
    Test the contains_substring function when the substring is present in the string.
    """
    # Test case 1: Substring is present in the string
    assert contains_substring("hello world", "world") == True, "Failed on substring present"

def test_contains_substring_not_present() -> None:
    """
    Test the contains_substring function when the substring is not present in the string.
    """
    # Test case 2: Substring is not present in the string
    assert contains_substring("hello world", "there") == False, "Failed on substring not present"

def test_contains_substring_entire_string() -> None:
    """
    Test the contains_substring function when the substring is the entire string.
    """
    # Test case 3: Substring is the entire string
    assert contains_substring("hello", "hello") == True, "Failed on substring is the entire string"

def test_contains_substring_empty_substring() -> None:
    """
    Test the contains_substring function when the substring is an empty string.
    """
    # Test case 4: Substring is an empty string
    assert contains_substring("hello", "") == True, "Failed on empty substring"

def test_contains_substring_empty_string() -> None:
    """
    Test the contains_substring function when the string is empty.
    """
    # Test case 5: String is an empty string
    assert contains_substring("", "hello") == False, "Failed on empty string"

def test_contains_substring_both_empty() -> None:
    """
    Test the contains_substring function when both the string and the substring are empty.
    """
    # Test case 6: Both string and substring are empty
    assert contains_substring("", "") == True, "Failed on both string and substring empty"

def test_contains_substring_beginning() -> None:
    """
    Test the contains_substring function when the substring is at the beginning of the string.
    """
    # Test case 7: Substring is at the beginning of the string
    assert contains_substring("hello world", "hello") == True, "Failed on substring at the beginning"

def test_contains_substring_end() -> None:
    """
    Test the contains_substring function when the substring is at the end of the string.
    """
    # Test case 8: Substring is at the end of the string
    assert contains_substring("hello world", "world") == True, "Failed on substring at the end"

def test_contains_substring_middle() -> None:
    """
    Test the contains_substring function when the substring is in the middle of the string.
    """
    # Test case 9: Substring is in the middle of the string
    assert contains_substring("hello world", "lo wo") == True, "Failed on substring in the middle"

def test_contains_substring_single_character_present() -> None:
    """
    Test the contains_substring function when the substring is a single character present in the string.
    """
    # Test case 10: Substring is a single character present in the string
    assert contains_substring("hello world", "o") == True, "Failed on single character present"

def test_contains_substring_single_character_not_present() -> None:
    """
    Test the contains_substring function when the substring is a single character not present in the string.
    """
    # Test case 11: Substring is a single character not present in the string
    assert contains_substring("hello world", "x") == False, "Failed on single character not present"

def test_contains_substring_special_characters() -> None:
    """
    Test the contains_substring function when the substring contains special characters.
    """
    # Test case 12: Substring with special characters
    assert contains_substring("hello!@# world", "!@#") == True, "Failed on substring with special characters"

def test_contains_substring_numbers() -> None:
    """
    Test the contains_substring function when the substring contains numbers.
    """
    # Test case 13: Substring with numbers
    assert contains_substring("hello123 world", "123") == True, "Failed on substring with numbers"

def test_contains_substring_mixed_case() -> None:
    """
    Test the contains_substring function when the substring has mixed case.
    """
    # Test case 14: Substring with mixed case
    assert contains_substring("Hello World", "world") == False, "Failed on mixed case substring"

def test_contains_substring_mixed_case_insensitive() -> None:
    """
    Test the contains_substring function when the substring has mixed case (case insensitive).
    """
    # Test case 15: Substring with mixed case (case insensitive)
    assert contains_substring("Hello World", "World") == True, "Failed on mixed case substring (case insensitive)"

def test_contains_substring_spaces() -> None:
    """
    Test the contains_substring function when the substring contains spaces.
    """
    # Test case 16: Substring with spaces
    assert contains_substring("hello world", " ") == True, "Failed on substring with spaces"

def test_contains_substring_newline_characters() -> None:
    """
    Test the contains_substring function when the substring contains newline characters.
    """
    # Test case 17: Substring with newline characters
    assert contains_substring("hello\nworld", "\n") == True, "Failed on substring with newline characters"

def test_contains_substring_tab_characters() -> None:
    """
    Test the contains_substring function when the substring contains tab characters.
    """
    # Test case 18: Substring with tab characters
    assert contains_substring("hello\tworld", "\t") == True, "Failed on substring with tab characters"

def test_contains_substring_leading_trailing_spaces() -> None:
    """
    Test the contains_substring function when the substring contains leading and trailing spaces.
    """
    # Test case 19: Substring with leading and trailing spaces
    assert contains_substring("  hello world  ", "hello") == True, "Failed on substring with leading and trailing spaces"

def test_contains_substring_punctuation() -> None:
    """
    Test the contains_substring function when the substring contains punctuation.
    """
    # Test case 20: Substring with punctuation
    assert contains_substring("hello, world!", "world!") == True, "Failed on substring with punctuation"

def test_contains_substring_non_english_characters() -> None:
    """
    Test the contains_substring function when the substring contains non-English characters.
    """
    # Test case 21: Substring with non-English characters
    assert contains_substring("héllo wörld", "wörld") == True, "Failed on substring with non-English characters"

def test_contains_substring_invalid_string_type() -> None:
    """
    Test the contains_substring function with an invalid string type.
    """
    # Test case 22: Invalid string type
    with pytest.raises(TypeError):
        contains_substring(12345, "hello")

def test_contains_substring_invalid_substring_type() -> None:
    """
    Test the contains_substring function with an invalid substring type.
    """
    # Test case 23: Invalid substring type
    with pytest.raises(TypeError):
        contains_substring("hello world", 123)


