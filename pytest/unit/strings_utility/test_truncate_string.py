import pytest
from strings_utility.truncate_string import truncate_string

def test_truncate_string_basic() -> None:
    """
    Test the truncate_string function with basic truncation.
    """
    # Test case 1: Basic truncation
    assert truncate_string("hello world", 5) == "hello", "Failed on basic truncation"

def test_truncate_string_length_greater_than_string() -> None:
    """
    Test the truncate_string function with length greater than the string length.
    """
    # Test case 2: Length greater than the string length
    assert truncate_string("abc", 5) == "abc", "Failed on length greater than the string length"

def test_truncate_string_length_equal_to_string() -> None:
    """
    Test the truncate_string function with length equal to the string length.
    """
    # Test case 3: Length equal to the string length
    assert truncate_string("hello", 5) == "hello", "Failed on length equal to the string length"

def test_truncate_string_length_zero() -> None:
    """
    Test the truncate_string function with length zero.
    """
    # Test case 4: Length zero
    assert truncate_string("hello", 0) == "", "Failed on length zero"

def test_truncate_string_empty_string() -> None:
    """
    Test the truncate_string function with an empty string.
    """
    # Test case 5: Empty string
    assert truncate_string("", 5) == "", "Failed on empty string"

def test_truncate_string_special_characters() -> None:
    """
    Test the truncate_string function with a string that contains special characters.
    """
    # Test case 6: String with special characters
    assert truncate_string("!@#hello$%^", 3) == "!@#", "Failed on string with special characters"

def test_truncate_string_numbers() -> None:
    """
    Test the truncate_string function with a string that contains numbers.
    """
    # Test case 7: String with numbers
    assert truncate_string("1234567890", 5) == "12345", "Failed on string with numbers"

def test_truncate_string_mixed_case() -> None:
    """
    Test the truncate_string function with a string that contains mixed case letters.
    """
    # Test case 8: String with mixed case letters
    assert truncate_string("HeLLoWoRLd", 7) == "HeLLoWo", "Failed on string with mixed case letters"

def test_truncate_string_non_english_characters() -> None:
    """
    Test the truncate_string function with a string that contains non-English characters.
    """
    # Test case 9: String with non-English characters
    assert truncate_string("héllo wörld", 5) == "héllo", "Failed on string with non-English characters"

def test_truncate_string_mixed_whitespace() -> None:
    """
    Test the truncate_string function with a string that contains mixed whitespace characters.
    """
    # Test case 10: String with mixed whitespace characters
    assert truncate_string(" \t\nhello world\t\n ", 8) == " \t\nhello", "Failed on string with mixed whitespace characters"

def test_truncate_string_negative_length() -> None:
    """
    Test the truncate_string function with a negative length.
    """
    # Test case 11: Negative length
    assert truncate_string("hello", -3) == "he", "Failed on negative length"

def test_truncate_string_invalid_string_type() -> None:
    """
    Test the truncate_string function with an invalid string type.
    """
    # Test case 12: Invalid string type
    with pytest.raises(TypeError):
        truncate_string(12345, 3)

def test_truncate_string_invalid_length_type() -> None:
    """
    Test the truncate_string function with an invalid length type.
    """
    # Test case 13: Invalid length type
    with pytest.raises(TypeError):
        truncate_string("hello", "3")


