import pytest
from strings_utility.is_palindrome import is_palindrome


def test_palindrome_odd_length() -> None:
    """
    Test case 1: Test the is_palindrome function with a palindrome of odd length.
    """
    assert is_palindrome("racecar"), "Failed on palindrome with odd length"


def test_palindrome_even_length() -> None:
    """
    Test case 2: Test the is_palindrome function with a palindrome of even length.
    """
    assert is_palindrome("abba"), "Failed on palindrome with even length"


def test_non_palindrome_odd_length() -> None:
    """
    Test case 3: Test the is_palindrome function with a non-palindrome of odd length.
    """
    assert not is_palindrome("hello"), "Failed on non-palindrome with odd length"


def test_non_palindrome_even_length() -> None:
    """
    Test case 4: Test the is_palindrome function with a non-palindrome of even length.
    """
    assert not is_palindrome("abcd"), "Failed on non-palindrome with even length"


def test_single_character() -> None:
    """
    Test case 5: Test the is_palindrome function with a single character string.
    """
    assert is_palindrome("a"), "Failed on single character string"


def test_empty_string() -> None:
    """
    Test case 6: Test the is_palindrome function with an empty string.
    """
    assert is_palindrome(""), "Failed on empty string"


def test_palindrome_mixed_case() -> None:
    """
    Test case 7: Test the is_palindrome function with a palindrome of mixed case.
    """
    assert not is_palindrome("RaceCar"), "Failed on palindrome with mixed case"


def test_palindrome_with_spaces() -> None:
    """
    Test case 8: Test the is_palindrome function with a palindrome that includes spaces.
    """
    assert not is_palindrome(
        "a man a plan a canal panama"
    ), "Failed on palindrome with spaces"


def test_palindrome_with_punctuation() -> None:
    """
    Test case 9: Test the is_palindrome function with a palindrome that includes punctuation.
    """
    assert not is_palindrome(
        "A man, a plan, a canal, Panama!"
    ), "Failed on palindrome with punctuation"


def test_palindrome_with_numbers() -> None:
    """
    Test case 10: Test the is_palindrome function with a palindrome that includes numbers.
    """
    assert is_palindrome("12321"), "Failed on palindrome with numbers"


def test_non_palindrome_with_numbers() -> None:
    """
    Test case 11: Test the is_palindrome function with a non-palindrome that includes numbers.
    """
    assert not is_palindrome("12345"), "Failed on non-palindrome with numbers"


def test_palindrome_with_special_characters() -> None:
    """
    Test case 12: Test the is_palindrome function with a palindrome that includes special characters.
    """
    assert is_palindrome("@#@"), "Failed on palindrome with special characters"


def test_non_palindrome_with_special_characters() -> None:
    """
    Test case 13: Test the is_palindrome function with a non-palindrome that includes special characters.
    """
    assert not is_palindrome("@#a"), "Failed on non-palindrome with special characters"


def test_palindrome_mixed_alphanumeric() -> None:
    """
    Test case 14: Test the is_palindrome function with a palindrome that includes mixed alphanumeric characters.
    """
    assert is_palindrome(
        "A1B2B1A"
    ), "Failed on palindrome with mixed alphanumeric characters"


def test_non_palindrome_mixed_alphanumeric() -> None:
    """
    Test case 15: Test the is_palindrome function with a non-palindrome that includes mixed alphanumeric characters.
    """
    assert not is_palindrome(
        "A1B2C3"
    ), "Failed on non-palindrome with mixed alphanumeric characters"


def test_palindrome_leading_trailing_spaces() -> None:
    """
    Test case 16: Test the is_palindrome function with a palindrome that includes leading and trailing spaces.
    """
    assert is_palindrome(
        " racecar "
    ), "Failed on palindrome with leading and trailing spaces"


def test_is_palindrome_invalid_type() -> None:
    """
    Test case 17: Test the is_palindrome function with an invalid type.
    """
    with pytest.raises(TypeError):
        is_palindrome(12345)
