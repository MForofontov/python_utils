import pytest
from strings_utility.capitalize_words import capitalize_words

def test_single_word() -> None:
    """
    Test the capitalize_words function with a single word.
    """
    # Test case 1: Single word
    assert capitalize_words("hello") == "Hello", "Failed on single word"

def test_multiple_words() -> None:
    """
    Test the capitalize_words function with multiple words.
    """
    # Test case 2: Multiple words
    assert capitalize_words("hello world") == "Hello World", "Failed on multiple words"

def test_mixed_case_words() -> None:
    """
    Test the capitalize_words function with mixed case words.
    """
    # Test case 3: Mixed case words
    assert capitalize_words("python programming") == "Python Programming", "Failed on mixed case words"

def test_all_uppercase_words() -> None:
    """
    Test the capitalize_words function with all uppercase words.
    """
    # Test case 4: All uppercase words
    assert capitalize_words("CAPITALIZE EACH WORD") == "Capitalize Each Word", "Failed on all uppercase words"

def test_all_lowercase_words() -> None:
    """
    Test the capitalize_words function with all lowercase words.
    """
    # Test case 5: All lowercase words
    assert capitalize_words("capitalize each word") == "Capitalize Each Word", "Failed on all lowercase words"

def test_words_with_punctuation() -> None:
    """
    Test the capitalize_words function with words that include punctuation.
    """
    # Test case 6: Words with punctuation
    assert capitalize_words("hello, world!") == "Hello, World!", "Failed on words with punctuation"

def test_words_with_numbers() -> None:
    """
    Test the capitalize_words function with words that include numbers.
    """
    # Test case 7: Words with numbers
    assert capitalize_words("hello world 123") == "Hello World 123", "Failed on words with numbers"

def test_empty_string() -> None:
    """
    Test the capitalize_words function with an empty string.
    """
    # Test case 8: Empty string
    assert capitalize_words("") == "", "Failed on empty string"

def test_string_with_only_spaces() -> None:
    """
    Test the capitalize_words function with a string that contains only spaces.
    """
    # Test case 9: String with only spaces
    assert capitalize_words("   ") == "   ", "Failed on string with only spaces"

def test_string_with_leading_and_trailing_spaces() -> None:
    """
    Test the capitalize_words function with a string that has leading and trailing spaces.
    """
    # Test case 10: String with leading and trailing spaces
    assert capitalize_words("  hello world  ") == "  Hello World  ", "Failed on string with leading and trailing spaces"

def test_string_with_mixed_whitespace_characters() -> None:
    """
    Test the capitalize_words function with a string that has mixed whitespace characters.
    """
    # Test case 11: String with mixed whitespace characters
    assert capitalize_words("hello\tworld\npython") == "Hello\tWorld\nPython", "Failed on string with mixed whitespace characters"

def test_string_with_special_characters() -> None:
    """
    Test the capitalize_words function with a string that has special characters.
    """
    # Test case 12: String with special characters
    assert capitalize_words("hello!@# world") == "Hello!@# World", "Failed on string with special characters"

def test_string_with_newline_characters() -> None:
    """
    Test the capitalize_words function with a string that has newline characters.
    """
    # Test case 13: String with newline characters
    assert capitalize_words("hello\nworld") == "Hello\nWorld", "Failed on string with newline characters"

def test_string_with_tab_characters() -> None:
    """
    Test the capitalize_words function with a string that has tab characters.
    """
    # Test case 14: String with tab characters
    assert capitalize_words("hello\tworld") == "Hello\tWorld", "Failed on string with tab characters"

def test_string_with_mixed_case_and_special_characters() -> None:
    """
    Test the capitalize_words function with a string that has mixed case and special characters.
    """
    # Test case 15: String with mixed case and special characters
    assert capitalize_words("hello!@# WORLD") == "Hello!@# World", "Failed on string with mixed case and special characters"

def test_string_with_leading_and_trailing_special_characters() -> None:
    """
    Test the capitalize_words function with a string that has leading and trailing special characters.
    """
    # Test case 16: String with leading and trailing special characters
    assert capitalize_words("!@#hello world!@#") == "!@#Hello World!@#", "Failed on string with leading and trailing special characters"

def test_string_with_mixed_case_and_numbers() -> None:
    """
    Test the capitalize_words function with a string that has mixed case and numbers.
    """
    # Test case 17: String with mixed case and numbers
    assert capitalize_words("hello123 world456") == "Hello123 World456", "Failed on string with mixed case and numbers"

def test_string_with_leading_and_trailing_numbers() -> None:
    """
    Test the capitalize_words function with a string that has leading and trailing numbers.
    """
    # Test case 18: String with leading and trailing numbers
    assert capitalize_words("123hello world456") == "123Hello World456", "Failed on string with leading and trailing numbers"

def test_string_with_mixed_case_and_punctuation() -> None:
    """
    Test the capitalize_words function with a string that has mixed case and punctuation.
    """
    # Test case 19: String with mixed case and punctuation
    assert capitalize_words("hello, world!") == "Hello, World!", "Failed on string with mixed case and punctuation"

def test_string_with_leading_and_trailing_punctuation() -> None:
    """
    Test the capitalize_words function with a string that has leading and trailing punctuation.
    """
    # Test case 20: String with leading and trailing punctuation
    assert capitalize_words(",hello world!") == ",Hello World!", "Failed on string with leading and trailing punctuation"

def test_capitalize_words_invalid_type() -> None:
    """
    Test the capitalize_words function with an invalid type.
    """
    # Test case 21: Invalid type
    with pytest.raises(TypeError):
        capitalize_words(12345)


