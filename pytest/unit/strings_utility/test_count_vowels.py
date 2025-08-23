import pytest
from strings_utility.count_vowels import count_vowels


def test_mixed_case_vowels_and_consonants() -> None:
    """
    Test the count_vowels function with mixed case vowels and consonants.
    """
    # Test case 1: String with mixed case vowels and consonants
    assert count_vowels(
        "hello") == 2, "Failed on mixed case vowels and consonants"
    # Test case 2: String with mixed case vowels
    assert count_vowels("HeLLo WoRLd") == 3, "Failed on mixed case vowels"
    # Test case 3: String with mixed case vowels and consonants
    assert (
        count_vowels("aEiOuBcDfGh") == 5
    ), "Failed on mixed case vowels and consonants"


def test_all_vowels() -> None:
    """
    Test the count_vowels function with all vowels.
    """
    # Test case 4: String with all vowels
    assert count_vowels("aeiouAEIOU") == 10, "Failed on all vowels"
    # Test case 5: String with only vowels
    assert count_vowels("aeiou") == 5, "Failed on string with only vowels"
    # Test case 6: String with only uppercase vowels
    assert count_vowels(
        "AEIOU") == 5, "Failed on string with only uppercase vowels"
    # Test case 7: String with repeated vowels
    assert (
        count_vowels("aaaeeeiiiooouuu") == 15
    ), "Failed on string with repeated vowels"


def test_all_consonants() -> None:
    """
    Test the count_vowels function with all consonants.
    """
    # Test case 8: String with all consonants
    assert (
        count_vowels("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ") == 0
    ), "Failed on all consonants"
    # Test case 9: String with no vowels
    assert count_vowels(
        "bcdfghjklmnpqrstvwxyz") == 0, "Failed on string with no vowels"


def test_empty_string() -> None:
    """
    Test the count_vowels function with an empty string.
    """
    # Test case 10: Empty string
    assert count_vowels("") == 0, "Failed on empty string"


def test_numbers_and_special_characters() -> None:
    """
    Test the count_vowels function with numbers and special characters.
    """
    # Test case 11: String with numbers and special characters
    assert (
        count_vowels("12345!@#$%") == 0
    ), "Failed on string with numbers and special characters"
    # Test case 12: String with mixed vowels, consonants, numbers, and special characters
    assert (
        count_vowels("h3llo w0rld!") == 1
    ), "Failed on mixed vowels, consonants, numbers, and special characters"
    # Test case 13: String with punctuation
    assert count_vowels(
        "hello, world!") == 3, "Failed on string with punctuation"
    # Test case 14: String with special characters
    assert count_vowels(
        "!@#hello!@#") == 2, "Failed on string with special characters"
    # Test case 15: String with numbers
    assert count_vowels("123hello123") == 2, "Failed on string with numbers"


def test_whitespace_characters() -> None:
    """
    Test the count_vowels function with whitespace characters.
    """
    # Test case 16: String with spaces
    assert count_vowels("hello world") == 3, "Failed on string with spaces"
    # Test case 17: String with newline characters
    assert count_vowels(
        "hello\nworld") == 3, "Failed on string with newline characters"
    # Test case 18: String with tab characters
    assert count_vowels(
        "hello\tworld") == 3, "Failed on string with tab characters"
    # Test case 19: String with mixed whitespace characters
    assert (
        count_vowels("hello \t\nworld") == 3
    ), "Failed on string with mixed whitespace characters"
    # Test case 20: String with leading and trailing spaces
    assert (
        count_vowels("  hello world  ") == 3
    ), "Failed on string with leading and trailing spaces"


def test_non_english_characters() -> None:
    """
    Test the count_vowels function with non-English characters.
    """
    # Test case 21: String with non-English characters
    assert (
        count_vowels("héllo wörld") == 1
    ), "Failed on string with non-English characters"


def test_count_vowels_invalid_type() -> None:
    """
    Test the count_vowels function with an invalid type.
    """
    # Test case 22: Invalid type
    with pytest.raises(TypeError):
        count_vowels(12345)
