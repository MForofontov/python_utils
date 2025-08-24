import pytest
from strings_utility.capitalize_words import capitalize_words


def test_single_word() -> None:
    """
    Test case 1: Test the capitalize_words function with a single word.
    """
    assert capitalize_words("hello") == "Hello", "Failed on single word"


def test_multiple_words() -> None:
    """
    Test case 2: Test the capitalize_words function with multiple words.
    """
    assert capitalize_words(
        "hello world") == "Hello World", "Failed on multiple words"


def test_mixed_case_words() -> None:
    """
    Test case 3: Test the capitalize_words function with mixed case words.
    """
    assert (
        capitalize_words("python programming") == "Python Programming"
    ), "Failed on mixed case words"


def test_all_uppercase_words() -> None:
    """
    Test case 4: Test the capitalize_words function with all uppercase words.
    """
    assert (
        capitalize_words("CAPITALIZE EACH WORD") == "Capitalize Each Word"
    ), "Failed on all uppercase words"


def test_all_lowercase_words() -> None:
    """
    Test case 5: Test the capitalize_words function with all lowercase words.
    """
    assert (
        capitalize_words("capitalize each word") == "Capitalize Each Word"
    ), "Failed on all lowercase words"


def test_words_with_punctuation() -> None:
    """
    Test case 6: Test the capitalize_words function with words that include punctuation.
    """
    assert (
        capitalize_words("hello, world!") == "Hello, World!"
    ), "Failed on words with punctuation"


def test_words_with_numbers() -> None:
    """
    Test case 7: Test the capitalize_words function with words that include numbers.
    """
    assert (
        capitalize_words("hello world 123") == "Hello World 123"
    ), "Failed on words with numbers"


def test_empty_string() -> None:
    """
    Test case 8: Test the capitalize_words function with an empty string.
    """
    assert capitalize_words("") == "", "Failed on empty string"


def test_string_with_only_spaces() -> None:
    """
    Test case 9: Test the capitalize_words function with a string that contains only spaces.
    """
    assert capitalize_words(
        "   ") == "   ", "Failed on string with only spaces"


def test_string_with_leading_and_trailing_spaces() -> None:
    """
    Test case 10: Test the capitalize_words function with a string that has leading and trailing spaces.
    """
    assert (
        capitalize_words("  hello world  ") == "  Hello World  "
    ), "Failed on string with leading and trailing spaces"


def test_string_with_mixed_whitespace_characters() -> None:
    """
    Test case 11: Test the capitalize_words function with a string that has mixed whitespace characters.
    """
    assert (
        capitalize_words("hello\tworld\npython") == "Hello\tWorld\nPython"
    ), "Failed on string with mixed whitespace characters"


def test_string_with_special_characters() -> None:
    """
    Test case 12: Test the capitalize_words function with a string that has special characters.
    """
    assert (
        capitalize_words("hello!@# world") == "Hello!@# World"
    ), "Failed on string with special characters"


def test_string_with_newline_characters() -> None:
    """
    Test case 13: Test the capitalize_words function with a string that has newline characters.
    """
    assert (
        capitalize_words("hello\nworld") == "Hello\nWorld"
    ), "Failed on string with newline characters"


def test_string_with_tab_characters() -> None:
    """
    Test case 14: Test the capitalize_words function with a string that has tab characters.
    """
    assert (
        capitalize_words("hello\tworld") == "Hello\tWorld"
    ), "Failed on string with tab characters"


def test_string_with_mixed_case_and_special_characters() -> None:
    """
    Test case 15: Test the capitalize_words function with a string that has mixed case and special characters.
    """
    assert (
        capitalize_words("hello!@# WORLD") == "Hello!@# World"
    ), "Failed on string with mixed case and special characters"


def test_string_with_leading_and_trailing_special_characters() -> None:
    """
    Test case 16: Test the capitalize_words function with a string that has leading and trailing special characters.
    """
    assert (
        capitalize_words("!@#hello world!@#") == "!@#Hello World!@#"
    ), "Failed on string with leading and trailing special characters"


def test_string_with_mixed_case_and_numbers() -> None:
    """
    Test case 17: Test the capitalize_words function with a string that has mixed case and numbers.
    """
    assert (
        capitalize_words("hello123 world456") == "Hello123 World456"
    ), "Failed on string with mixed case and numbers"


def test_string_with_leading_and_trailing_numbers() -> None:
    """
    Test case 18: Test the capitalize_words function with a string that has leading and trailing numbers.
    """
    assert (
        capitalize_words("123hello world456") == "123Hello World456"
    ), "Failed on string with leading and trailing numbers"


def test_string_with_mixed_case_and_punctuation() -> None:
    """
    Test case 19: Test the capitalize_words function with a string that has mixed case and punctuation.
    """
    assert (
        capitalize_words("hello, world!") == "Hello, World!"
    ), "Failed on string with mixed case and punctuation"


def test_string_with_leading_and_trailing_punctuation() -> None:
    """
    Test case 20: Test the capitalize_words function with a string that has leading and trailing punctuation.
    """
    assert (
        capitalize_words(",hello world!") == ",Hello World!"
    ), "Failed on string with leading and trailing punctuation"


def test_capitalize_words_invalid_type() -> None:
    """
    Test case 21: Test the capitalize_words function with an invalid type.
    """
    with pytest.raises(TypeError):
        capitalize_words(12345)
