import pytest
from strings_utility.is_palindrome import is_palindrome


def test_palindrome_odd_length() -> None:
    """
    Test case 1: Test the is_palindrome function with a palindrome of odd length.
    """
    assert is_palindrome(
        "racecar") == True, "Failed on palindrome with odd length"


def test_palindrome_even_length() -> None:
    """
    Test case 2: Test the is_palindrome function with a palindrome of even length.
    """
    assert is_palindrome(
        "abba") == True, "Failed on palindrome with even length"


def test_non_palindrome_odd_length() -> None:
    """
    Test case 3: Test the is_palindrome function with a non-palindrome of odd length.
    """
    assert is_palindrome(
        "hello") == False, "Failed on non-palindrome with odd length"


def test_non_palindrome_even_length() -> None:
    """
    Test case 4: Test the is_palindrome function with a non-palindrome of even length.
    """
    assert is_palindrome(
        "abcd") == False, "Failed on non-palindrome with even length"


def test_single_character() -> None:
    """
    Test case 5: Test the is_palindrome function with a single character string.
    """
    assert is_palindrome("a") == True, "Failed on single character string"


def test_empty_string() -> None:
    """
    Test case 6: Test the is_palindrome function with an empty string.
    """
    assert is_palindrome("") == True, "Failed on empty string"


def test_palindrome_mixed_case() -> None:
    """
    Test case 7: Test the is_palindrome function with a palindrome of mixed case.
    """
    assert is_palindrome(
        "RaceCar") == False, "Failed on palindrome with mixed case"


def test_palindrome_with_spaces() -> None:
    """
    Test case 8: Test the is_palindrome function with a palindrome that includes spaces.
    """
    assert (
        is_palindrome("a man a plan a canal panama") == False
    ), "Failed on palindrome with spaces"


def test_palindrome_with_punctuation() -> None:
    """
    Test case 9: Test the is_palindrome function with a palindrome that includes punctuation.
    """
    assert (
        is_palindrome("A man, a plan, a canal, Panama!") == False
    ), "Failed on palindrome with punctuation"


def test_palindrome_with_numbers() -> None:
    """
    Test case 10: Test the is_palindrome function with a palindrome that includes numbers.
    """
    assert is_palindrome("12321") == True, "Failed on palindrome with numbers"


def test_non_palindrome_with_numbers() -> None:
    """
    Test case 11: Test the is_palindrome function with a non-palindrome that includes numbers.
    """
    assert is_palindrome(
        "12345") == False, "Failed on non-palindrome with numbers"


def test_palindrome_with_special_characters() -> None:
    """
    Test case 12: Test the is_palindrome function with a palindrome that includes special characters.
    """
    assert is_palindrome(
        "@#@") == True, "Failed on palindrome with special characters"


def test_non_palindrome_with_special_characters() -> None:
    """
    Test case 13: Test the is_palindrome function with a non-palindrome that includes special characters.
    """
    assert (
        is_palindrome("@#a") == False
    ), "Failed on non-palindrome with special characters"


def test_palindrome_mixed_alphanumeric() -> None:
    """
    Test case 14: Test the is_palindrome function with a palindrome that includes mixed alphanumeric characters.
    """
    assert (
        is_palindrome("A1B2B1A") == True
    ), "Failed on palindrome with mixed alphanumeric characters"


def test_non_palindrome_mixed_alphanumeric() -> None:
    """
    Test case 15: Test the is_palindrome function with a non-palindrome that includes mixed alphanumeric characters.
    """
    assert (
        is_palindrome("A1B2C3") == False
    ), "Failed on non-palindrome with mixed alphanumeric characters"


def test_palindrome_leading_trailing_spaces() -> None:
    """
    Test case 16: Test the is_palindrome function with a palindrome that includes leading and trailing spaces.
    """
    assert (
        is_palindrome(" racecar ") == True
    ), "Failed on palindrome with leading and trailing spaces"


def test_palindrome_with_newline_characters() -> None:
    """
    Test case 17: Test the is_palindrome function with a palindrome that includes newline characters.
    """
    assert (
        is_palindrome("race\ncar") == False
    ), "Failed on palindrome with newline characters"


def test_palindrome_with_tab_characters() -> None:
    """
    Test case 18: Test the is_palindrome function with a palindrome that includes tab characters.
    """
    assert (
        is_palindrome("race\tcar") == False
    ), "Failed on palindrome with tab characters"


def test_palindrome_mixed_whitespace() -> None:
    """
    Test case 19: Test the is_palindrome function with a palindrome that includes mixed whitespace characters.
    """
    assert (
        is_palindrome("race \t\ncar") == False
    ), "Failed on palindrome with mixed whitespace characters"


def test_is_palindrome_invalid_type() -> None:
    """
    Test case 20: Test the is_palindrome function with an invalid type.
    """
    with pytest.raises(TypeError):
        is_palindrome(12345)
