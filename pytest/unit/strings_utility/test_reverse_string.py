import pytest
from strings_utility.reverse_string import reverse_string


def test_reverse_string_basic() -> None:
    """
    Test case 1: Test the reverse_string function with a basic string.
    """
    assert reverse_string("hello") == "olleh", "Failed on basic string"


def test_reverse_string_empty() -> None:
    """
    Test case 2: Test the reverse_string function with an empty string.
    """
    assert reverse_string("") == "", "Failed on empty string"


def test_reverse_string_single_character() -> None:
    """
    Test case 3: Test the reverse_string function with a single character string.
    """
    assert reverse_string("a") == "a", "Failed on single character string"


def test_reverse_string_palindrome() -> None:
    """
    Test case 4: Test the reverse_string function with a palindrome.
    """
    assert reverse_string("racecar") == "racecar", "Failed on palindrome"


def test_reverse_string_whitespace() -> None:
    """
    Test case 5: Test the reverse_string function with a string that contains whitespace.
    """
    assert (
        reverse_string("hello world") == "dlrow olleh"
    ), "Failed on string with whitespace"


def test_reverse_string_special_characters() -> None:
    """
    Test case 6: Test the reverse_string function with a string that contains special characters.
    """
    assert (
        reverse_string("hello!@#") == "#@!olleh"
    ), "Failed on string with special characters"


def test_reverse_string_numbers() -> None:
    """
    Test case 7: Test the reverse_string function with a string that contains numbers.
    """
    assert reverse_string("12345") == "54321", "Failed on string with numbers"


def test_reverse_string_mixed_case() -> None:
    """
    Test case 8: Test the reverse_string function with a string that contains mixed case letters.
    """
    assert (
        reverse_string("HelloWorld") == "dlroWolleH"
    ), "Failed on string with mixed case letters"


def test_reverse_string_non_english_characters() -> None:
    """
    Test case 9: Test the reverse_string function with a string that contains non-English characters.
    """
    assert (
        reverse_string("héllo wörld") == "dlröw olléh"
    ), "Failed on string with non-English characters"


def test_reverse_string_mixed_whitespace() -> None:
    """
    Test case 10: Test the reverse_string function with a string that contains mixed whitespace characters.
    """
    assert (
        reverse_string("hello \t\nworld") == "dlrow\n\t olleh"
    ), "Failed on string with mixed whitespace characters"


def test_reverse_string_invalid_type() -> None:
    """
    Test case 11: Test the reverse_string function with an invalid type.
    """
    with pytest.raises(TypeError):
        reverse_string(12345)
