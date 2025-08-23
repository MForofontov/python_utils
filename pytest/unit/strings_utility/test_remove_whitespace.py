import pytest
from strings_utility.remove_whitespace import remove_whitespace


def test_remove_whitespace_mixed_characters() -> None:
    """
    Test the remove_whitespace function with a string that contains both letters and whitespace characters.
    """
    # Test case 1: String with mixed letters and whitespace characters
    assert (
        remove_whitespace("hello world") == "helloworld"
    ), "Failed on mixed letters and whitespace characters"


def test_remove_whitespace_only_whitespace() -> None:
    """
    Test the remove_whitespace function with a string that contains only whitespace characters.
    """
    # Test case 2: String with only whitespace characters
    assert (
        remove_whitespace("     ") == ""
    ), "Failed on string with only whitespace characters"


def test_remove_whitespace_only_letters() -> None:
    """
    Test the remove_whitespace function with a string that contains only letters.
    """
    # Test case 3: String with only letters
    assert remove_whitespace(
        "abcdef") == "abcdef", "Failed on string with only letters"


def test_remove_whitespace_empty_string() -> None:
    """
    Test the remove_whitespace function with an empty string.
    """
    # Test case 4: Empty string
    assert remove_whitespace("") == "", "Failed on empty string"


def test_remove_whitespace_newline_characters() -> None:
    """
    Test the remove_whitespace function with a string that contains newline characters.
    """
    # Test case 5: String with newline characters
    assert (
        remove_whitespace("hello\nworld") == "helloworld"
    ), "Failed on string with newline characters"


def test_remove_whitespace_tab_characters() -> None:
    """
    Test the remove_whitespace function with a string that contains tab characters.
    """
    # Test case 6: String with tab characters
    assert (
        remove_whitespace("hello\tworld") == "helloworld"
    ), "Failed on string with tab characters"


def test_remove_whitespace_mixed_whitespace_characters() -> None:
    """
    Test the remove_whitespace function with a string that contains mixed whitespace characters.
    """
    # Test case 7: String with mixed whitespace characters
    assert (
        remove_whitespace("hello \t\nworld") == "helloworld"
    ), "Failed on string with mixed whitespace characters"


def test_remove_whitespace_leading_trailing_spaces() -> None:
    """
    Test the remove_whitespace function with a string that contains leading and trailing spaces.
    """
    # Test case 8: String with leading and trailing spaces
    assert (
        remove_whitespace(" hello world ") == "helloworld"
    ), "Failed on string with leading and trailing spaces"


def test_remove_whitespace_non_english_characters() -> None:
    """
    Test the remove_whitespace function with a string that contains non-English characters.
    """
    # Test case 9: String with non-English characters
    assert (
        remove_whitespace("héllo wörld") == "héllowörld"
    ), "Failed on string with non-English characters"


def test_remove_whitespace_mixed_case() -> None:
    """
    Test the remove_whitespace function with a string that contains mixed case letters.
    """
    # Test case 10: String with mixed case letters
    assert (
        remove_whitespace("Hello World") == "HelloWorld"
    ), "Failed on string with mixed case letters"


def test_remove_whitespace_numbers() -> None:
    """
    Test the remove_whitespace function with a string that contains numbers.
    """
    # Test case 11: String with numbers
    assert remove_whitespace(
        "123 456") == "123456", "Failed on string with numbers"


def test_remove_whitespace_numbers_within_words() -> None:
    """
    Test the remove_whitespace function with a string that contains numbers within words.
    """
    # Test case 12: String with numbers within words
    assert (
        remove_whitespace("a1b2c3") == "a1b2c3"
    ), "Failed on string with numbers within words"


def test_remove_whitespace_numbers_at_start_and_end() -> None:
    """
    Test the remove_whitespace function with a string that contains numbers at the start and end.
    """
    # Test case 13: String with numbers at the start and end
    assert (
        remove_whitespace("123abc456") == "123abc456"
    ), "Failed on string with numbers at the start and end"


def test_remove_whitespace_special_characters() -> None:
    """
    Test the remove_whitespace function with a string that contains special characters.
    """
    # Test case 14: String with special characters
    assert (
        remove_whitespace("hello!@# world") == "hello!@#world"
    ), "Failed on string with special characters"


def test_remove_whitespace_invalid_type() -> None:
    """
    Test the remove_whitespace function with an invalid type.
    """
    # Test case 15: Invalid type
    with pytest.raises(TypeError):
        remove_whitespace(123)
