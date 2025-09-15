import pytest
from strings_utility.remove_punctuation import remove_punctuation


def test_remove_punctuation_mixed_characters() -> None:
    """
    Test case 1: Test the remove_punctuation function with a string that contains both letters and punctuation.
    """
    assert remove_punctuation("hello, world!") == "hello world", (
        "Failed on mixed letters and punctuation"
    )


def test_remove_punctuation_only_punctuation() -> None:
    """
    Test case 2: Test the remove_punctuation function with a string that contains only punctuation.
    """
    assert remove_punctuation("!@#$%^&*()") == "", (
        "Failed on string with only punctuation"
    )


def test_remove_punctuation_only_letters() -> None:
    """
    Test case 3: Test the remove_punctuation function with a string that contains only letters.
    """
    assert remove_punctuation("abcdef") == "abcdef", (
        "Failed on string with only letters"
    )


def test_remove_punctuation_empty_string() -> None:
    """
    Test case 4: Test the remove_punctuation function with an empty string.
    """
    assert remove_punctuation("") == "", "Failed on empty string"


def test_remove_punctuation_whitespace_characters() -> None:
    """
    Test case 5: Test the remove_punctuation function with a string that contains whitespace characters.
    """
    assert remove_punctuation("hello world") == "hello world", (
        "Failed on string with whitespace characters"
    )


def test_remove_punctuation_newline_characters() -> None:
    """
    Test case 6: Test the remove_punctuation function with a string that contains newline characters.
    """
    assert remove_punctuation("hello\nworld") == "hello\nworld", (
        "Failed on string with newline characters"
    )


def test_remove_punctuation_tab_characters() -> None:
    """
    Test case 7: Test the remove_punctuation function with a string that contains tab characters.
    """
    assert remove_punctuation("hello\tworld") == "hello\tworld", (
        "Failed on string with tab characters"
    )


def test_remove_punctuation_mixed_whitespace_characters() -> None:
    """
    Test case 8: Test the remove_punctuation function with a string that contains mixed whitespace characters.
    """
    assert remove_punctuation("hello \t\nworld") == "hello \t\nworld", (
        "Failed on string with mixed whitespace characters"
    )


def test_remove_punctuation_leading_trailing_spaces() -> None:
    """
    Test case 9: Test the remove_punctuation function with a string that contains leading and trailing spaces.
    """
    assert remove_punctuation(" hello world ") == " hello world ", (
        "Failed on string with leading and trailing spaces"
    )


def test_remove_punctuation_non_english_characters() -> None:
    """
    Test case 10: Test the remove_punctuation function with a string that contains non-English characters.
    """
    assert remove_punctuation("héllo, wörld!") == "héllo wörld", (
        "Failed on string with non-English characters"
    )


def test_remove_punctuation_mixed_case() -> None:
    """
    Test case 11: Test the remove_punctuation function with a string that contains mixed case letters.
    """
    assert remove_punctuation("Hello, World!") == "Hello World", (
        "Failed on string with mixed case letters"
    )


def test_remove_punctuation_numbers() -> None:
    """
    Test case 12: Test the remove_punctuation function with a string that contains numbers.
    """
    assert remove_punctuation("123, 456!") == "123 456", "Failed on string with numbers"


def test_remove_punctuation_numbers_within_words() -> None:
    """
    Test case 13: Test the remove_punctuation function with a string that contains numbers within words.
    """
    assert remove_punctuation("a1b2c3!") == "a1b2c3", (
        "Failed on string with numbers within words"
    )


def test_remove_punctuation_numbers_at_start_and_end() -> None:
    """
    Test case 14: Test the remove_punctuation function with a string that contains numbers at the start and end.
    """
    assert remove_punctuation("123abc456!") == "123abc456", (
        "Failed on string with numbers at the start and end"
    )


def test_remove_punctuation_special_characters() -> None:
    """
    Test case 15: Test the remove_punctuation function with a string that contains special characters.
    """
    assert remove_punctuation("hello!@#world") == "helloworld", (
        "Failed on string with special characters"
    )


def test_remove_punctuation_invalid_type() -> None:
    """
    Test case 16: Test the remove_punctuation function with an invalid type.
    """
    with pytest.raises(TypeError):
        remove_punctuation(123)
