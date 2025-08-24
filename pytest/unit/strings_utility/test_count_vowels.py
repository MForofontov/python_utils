import pytest
from strings_utility.count_vowels import count_vowels


def test_mixed_case_vowels_and_consonants() -> None:
    assert count_vowels(
        "hello") == 2, "Failed on mixed case vowels and consonants"
    assert count_vowels("HeLLo WoRLd") == 3, "Failed on mixed case vowels"
    """
    Test case 3: Test the count_vowels function with mixed case vowels and consonants.
    """
    assert (
        count_vowels("aEiOuBcDfGh") == 5
    ), "Failed on mixed case vowels and consonants"


def test_all_vowels() -> None:
    assert count_vowels("aeiouAEIOU") == 10, "Failed on all vowels"
    assert count_vowels("aeiou") == 5, "Failed on string with only vowels"
    assert count_vowels(
        "AEIOU") == 5, "Failed on string with only uppercase vowels"
    """
    Test case 7: Test the count_vowels function with all vowels.
    """
    assert (
        count_vowels("aaaeeeiiiooouuu") == 15
    ), "Failed on string with repeated vowels"


def test_all_consonants() -> None:
    assert (
        count_vowels("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ") == 0
    ), "Failed on all consonants"
    """
    Test case 9: Test the count_vowels function with all consonants.
    """
    assert count_vowels(
        "bcdfghjklmnpqrstvwxyz") == 0, "Failed on string with no vowels"


def test_empty_string() -> None:
    """
    Test case 10: Test the count_vowels function with an empty string.
    """
    assert count_vowels("") == 0, "Failed on empty string"


def test_numbers_and_special_characters() -> None:
    assert (
        count_vowels("12345!@#$%") == 0
    ), "Failed on string with numbers and special characters"
    assert (
        count_vowels("h3llo w0rld!") == 1
    ), "Failed on mixed vowels, consonants, numbers, and special characters"
    assert count_vowels(
        "hello, world!") == 3, "Failed on string with punctuation"
    assert count_vowels(
        "!@#hello!@#") == 2, "Failed on string with special characters"
    """
    Test case 15: Test the count_vowels function with numbers and special characters.
    """
    assert count_vowels("123hello123") == 2, "Failed on string with numbers"


def test_whitespace_characters() -> None:
    assert count_vowels("hello world") == 3, "Failed on string with spaces"
    assert count_vowels(
        "hello\nworld") == 3, "Failed on string with newline characters"
    assert count_vowels(
        "hello\tworld") == 3, "Failed on string with tab characters"
    assert (
        count_vowels("hello \t\nworld") == 3
    ), "Failed on string with mixed whitespace characters"
    """
    Test case 20: Test the count_vowels function with whitespace characters.
    """
    assert (
        count_vowels("  hello world  ") == 3
    ), "Failed on string with leading and trailing spaces"


def test_non_english_characters() -> None:
    """
    Test case 21: Test the count_vowels function with non-English characters.
    """
    assert (
        count_vowels("héllo wörld") == 1
    ), "Failed on string with non-English characters"


def test_count_vowels_invalid_type() -> None:
    """
    Test case 22: Test the count_vowels function with an invalid type.
    """
    with pytest.raises(TypeError):
        count_vowels(12345)
