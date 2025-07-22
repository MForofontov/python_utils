import pytest
from strings_utility.remove_punctuation import remove_punctuation

def test_remove_punctuation_mixed_characters() -> None:
    """
    Test the remove_punctuation function with a string that contains both letters and punctuation.
    """
    # Test case 1: String with mixed letters and punctuation
    assert remove_punctuation("hello, world!") == "hello world", "Failed on mixed letters and punctuation"

def test_remove_punctuation_only_punctuation() -> None:
    """
    Test the remove_punctuation function with a string that contains only punctuation.
    """
    # Test case 2: String with only punctuation
    assert remove_punctuation("!@#$%^&*()") == "", "Failed on string with only punctuation"

def test_remove_punctuation_only_letters() -> None:
    """
    Test the remove_punctuation function with a string that contains only letters.
    """
    # Test case 3: String with only letters
    assert remove_punctuation("abcdef") == "abcdef", "Failed on string with only letters"

def test_remove_punctuation_empty_string() -> None:
    """
    Test the remove_punctuation function with an empty string.
    """
    # Test case 4: Empty string
    assert remove_punctuation("") == "", "Failed on empty string"

def test_remove_punctuation_whitespace_characters() -> None:
    """
    Test the remove_punctuation function with a string that contains whitespace characters.
    """
    # Test case 5: String with whitespace characters
    assert remove_punctuation("hello world") == "hello world", "Failed on string with whitespace characters"

def test_remove_punctuation_newline_characters() -> None:
    """
    Test the remove_punctuation function with a string that contains newline characters.
    """
    # Test case 6: String with newline characters
    assert remove_punctuation("hello\nworld") == "hello\nworld", "Failed on string with newline characters"

def test_remove_punctuation_tab_characters() -> None:
    """
    Test the remove_punctuation function with a string that contains tab characters.
    """
    # Test case 7: String with tab characters
    assert remove_punctuation("hello\tworld") == "hello\tworld", "Failed on string with tab characters"

def test_remove_punctuation_mixed_whitespace_characters() -> None:
    """
    Test the remove_punctuation function with a string that contains mixed whitespace characters.
    """
    # Test case 8: String with mixed whitespace characters
    assert remove_punctuation("hello \t\nworld") == "hello \t\nworld", "Failed on string with mixed whitespace characters"

def test_remove_punctuation_leading_trailing_spaces() -> None:
    """
    Test the remove_punctuation function with a string that contains leading and trailing spaces.
    """
    # Test case 9: String with leading and trailing spaces
    assert remove_punctuation(" hello world ") == " hello world ", "Failed on string with leading and trailing spaces"

def test_remove_punctuation_non_english_characters() -> None:
    """
    Test the remove_punctuation function with a string that contains non-English characters.
    """
    # Test case 10: String with non-English characters
    assert remove_punctuation("héllo, wörld!") == "héllo wörld", "Failed on string with non-English characters"

def test_remove_punctuation_mixed_case() -> None:
    """
    Test the remove_punctuation function with a string that contains mixed case letters.
    """
    # Test case 11: String with mixed case letters
    assert remove_punctuation("Hello, World!") == "Hello World", "Failed on string with mixed case letters"

def test_remove_punctuation_numbers() -> None:
    """
    Test the remove_punctuation function with a string that contains numbers.
    """
    # Test case 12: String with numbers
    assert remove_punctuation("123, 456!") == "123 456", "Failed on string with numbers"

def test_remove_punctuation_numbers_within_words() -> None:
    """
    Test the remove_punctuation function with a string that contains numbers within words.
    """
    # Test case 13: String with numbers within words
    assert remove_punctuation("a1b2c3!") == "a1b2c3", "Failed on string with numbers within words"

def test_remove_punctuation_numbers_at_start_and_end() -> None:
    """
    Test the remove_punctuation function with a string that contains numbers at the start and end.
    """
    # Test case 14: String with numbers at the start and end
    assert remove_punctuation("123abc456!") == "123abc456", "Failed on string with numbers at the start and end"

def test_remove_punctuation_special_characters() -> None:
    """
    Test the remove_punctuation function with a string that contains special characters.
    """
    # Test case 15: String with special characters
    assert remove_punctuation("hello!@#world") == "helloworld", "Failed on string with special characters"

def test_remove_punctuation_invalid_type() -> None:
    """
    Test the remove_punctuation function with an invalid type.
    """
    # Test case 16: Invalid type
    with pytest.raises(TypeError):
        remove_punctuation(123)


