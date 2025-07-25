import pytest
from strings_utility.reverse_string import reverse_string


def test_reverse_string_basic() -> None:
    """
    Test the reverse_string function with a basic string.
    """
    # Test case 1: Basic string
    assert reverse_string("hello") == "olleh", "Failed on basic string"


def test_reverse_string_empty() -> None:
    """
    Test the reverse_string function with an empty string.
    """
    # Test case 2: Empty string
    assert reverse_string("") == "", "Failed on empty string"


def test_reverse_string_single_character() -> None:
    """
    Test the reverse_string function with a single character string.
    """
    # Test case 3: Single character string
    assert reverse_string("a") == "a", "Failed on single character string"


def test_reverse_string_palindrome() -> None:
    """
    Test the reverse_string function with a palindrome.
    """
    # Test case 4: Palindrome
    assert reverse_string("racecar") == "racecar", "Failed on palindrome"


def test_reverse_string_whitespace() -> None:
    """
    Test the reverse_string function with a string that contains whitespace.
    """
    # Test case 5: String with whitespace
    assert (
        reverse_string("hello world") == "dlrow olleh"
    ), "Failed on string with whitespace"


def test_reverse_string_special_characters() -> None:
    """
    Test the reverse_string function with a string that contains special characters.
    """
    # Test case 6: String with special characters
    assert (
        reverse_string("hello!@#") == "#@!olleh"
    ), "Failed on string with special characters"


def test_reverse_string_numbers() -> None:
    """
    Test the reverse_string function with a string that contains numbers.
    """
    # Test case 7: String with numbers
    assert reverse_string("12345") == "54321", "Failed on string with numbers"


def test_reverse_string_mixed_case() -> None:
    """
    Test the reverse_string function with a string that contains mixed case letters.
    """
    # Test case 8: String with mixed case letters
    assert (
        reverse_string("HelloWorld") == "dlroWolleH"
    ), "Failed on string with mixed case letters"


def test_reverse_string_non_english_characters() -> None:
    """
    Test the reverse_string function with a string that contains non-English characters.
    """
    # Test case 9: String with non-English characters
    assert (
        reverse_string("héllo wörld") == "dlröw olléh"
    ), "Failed on string with non-English characters"


def test_reverse_string_mixed_whitespace() -> None:
    """
    Test the reverse_string function with a string that contains mixed whitespace characters.
    """
    # Test case 10: String with mixed whitespace characters
    assert (
        reverse_string("hello \t\nworld") == "dlrow\n\t olleh"
    ), "Failed on string with mixed whitespace characters"


def test_reverse_string_invalid_type() -> None:
    """
    Test the reverse_string function with an invalid type.
    """
    # Test case 11: Invalid type
    with pytest.raises(TypeError):
        reverse_string(12345)
