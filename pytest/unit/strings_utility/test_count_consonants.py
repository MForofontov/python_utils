import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from python_utils.strings_utility.count_consonants import count_consonants


def test_mixed_case_consonants_and_vowels() -> None:
    """
    Test case 1: Mixed case consonants and vowels.
    """
    assert count_consonants("hello") == 3, "Failed on mixed case consonants and vowels"
    # Additional scenario: ensure mixed case strings count consonants correctly.
    assert count_consonants("HeLLo WoRLd") == 7, "Failed on mixed case consonants"


def test_all_consonants() -> None:
    """
    Test case 2: All consonants.
    """
    assert count_consonants("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ") == 42, (
        "Failed on all consonants"
    )
    assert count_consonants("bcdfghjklmnpqrstvwxyz") == 21, (
        "Failed on string with only consonants"
    )
    assert count_consonants("BCDFGHJKLMNPQRSTVWXYZ") == 21, (
        "Failed on string with only uppercase consonants"
    )
    # Additional scenario: repeated consonants maintain correct counts.
    assert count_consonants("bbccddffgghhjjkkllmmnnppqqrrssttvvwwxxyyzz") == 42, (
        "Failed on string with repeated consonants"
    )


def test_all_vowels() -> None:
    """
    Test case 3: Test the count_consonants function with all vowels.
    """
    assert count_consonants("aeiouAEIOU") == 0, "Failed on all vowels"


def test_empty_string() -> None:
    """
    Test case 4: Test the count_consonants function with an empty string.
    """
    assert count_consonants("") == 0, "Failed on empty string"


def test_numbers_and_special_characters() -> None:
    """
    Test case 5: Numbers and special characters.
    """
    assert count_consonants("12345!@#$%") == 0, (
        "Failed on string with numbers and special characters"
    )
    assert count_consonants("h3ll0 w0rld!") == 7, (
        "Failed on mixed consonants, vowels, numbers, and special characters"
    )
    assert count_consonants("hello, world!") == 7, "Failed on string with punctuation"
    assert count_consonants("!@#hello!@#") == 3, (
        "Failed on string with special characters"
    )
    # Additional scenario: mixed alphanumeric strings count consonants correctly.
    assert count_consonants("123hello123") == 3, "Failed on string with numbers"


def test_whitespace_characters() -> None:
    """
    Test case 6: Whitespace characters.
    """
    assert count_consonants("hello world") == 7, "Failed on string with spaces"
    assert count_consonants("hello\nworld") == 7, (
        "Failed on string with newline characters"
    )
    assert count_consonants("hello\tworld") == 7, "Failed on string with tab characters"
    assert count_consonants("hello \t\nworld") == 7, (
        "Failed on string with mixed whitespace characters"
    )
    # Additional scenario: leading and trailing spaces are ignored in counts.
    assert count_consonants("  hello world  ") == 7, (
        "Failed on string with leading and trailing spaces"
    )


def test_non_english_characters() -> None:
    """
    Test case 7: Test the count_consonants function with non-English characters.
    """
    assert count_consonants("héllo wörld") == 7, (
        "Failed on string with non-English characters"
    )


def test_count_consonants_invalid_type() -> None:
    """
    Test case 8: Test the count_consonants function with an invalid type.
    """
    with pytest.raises(TypeError):
        count_consonants(12345)
