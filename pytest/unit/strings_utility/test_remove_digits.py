import pytest
from strings_utility.remove_digits import remove_digits


def test_remove_digits_basic() -> None:
    """
    Test the remove_digits function with a basic string containing digits.
    """
    # Test case 1: Basic string containing digits
    assert (
        remove_digits("hello123") == "hello"
    ), "Failed on basic string containing digits"


def test_remove_digits_all_digits() -> None:
    """
    Test the remove_digits function with a string that contains only digits.
    """
    # Test case 2: String with only digits
    assert remove_digits("12345") == "", "Failed on string with only digits"


def test_remove_digits_no_digits() -> None:
    """
    Test the remove_digits function with a string that contains no digits.
    """
    # Test case 3: String with no digits
    assert remove_digits("hello") == "hello", "Failed on string with no digits"


def test_remove_digits_empty_string() -> None:
    """
    Test the remove_digits function with an empty string.
    """
    # Test case 4: Empty string
    assert remove_digits("") == "", "Failed on empty string"


def test_remove_digits_special_characters() -> None:
    """
    Test the remove_digits function with a string that contains special characters.
    """
    # Test case 5: String with special characters
    assert (
        remove_digits("hello!@#123") == "hello!@#"
    ), "Failed on string with special characters"


def test_remove_digits_mixed_case() -> None:
    """
    Test the remove_digits function with a string that contains mixed case letters.
    """
    # Test case 6: String with mixed case letters
    assert (
        remove_digits("HeLLo123") == "HeLLo"
    ), "Failed on string with mixed case letters"


def test_remove_digits_non_english_characters() -> None:
    """
    Test the remove_digits function with a string that contains non-English characters.
    """
    # Test case 7: String with non-English characters
    assert (
        remove_digits("héllo123") == "héllo"
    ), "Failed on string with non-English characters"


def test_remove_digits_mixed_whitespace() -> None:
    """
    Test the remove_digits function with a string that contains mixed whitespace characters.
    """
    # Test case 8: String with mixed whitespace characters
    assert (
        remove_digits("hello \t\n123") == "hello \t\n"
    ), "Failed on string with mixed whitespace characters"


def test_remove_digits_only_digits() -> None:
    """
    Test the remove_digits function with a string that contains only digits.
    """
    # Test case 9: String with only digits
    assert remove_digits(
        "1234567890") == "", "Failed on string with only digits"


def test_remove_digits_digits_at_start() -> None:
    """
    Test the remove_digits function with a string that has digits at the start.
    """
    # Test case 10: String with digits at the start
    assert (
        remove_digits("123hello") == "hello"
    ), "Failed on string with digits at the start"


def test_remove_digits_digits_at_end() -> None:
    """
    Test the remove_digits function with a string that has digits at the end.
    """
    # Test case 11: String with digits at the end
    assert (
        remove_digits("hello123") == "hello"
    ), "Failed on string with digits at the end"


def test_remove_digits_digits_in_middle() -> None:
    """
    Test the remove_digits function with a string that has digits in the middle.
    """
    # Test case 12: String with digits in the middle
    assert (
        remove_digits("he123llo") == "hello"
    ), "Failed on string with digits in the middle"


def test_remove_digits_invalid_type() -> None:
    """
    Test the remove_digits function with an invalid type.
    """
    # Test case 13: Invalid type
    with pytest.raises(TypeError):
        remove_digits(12345)
