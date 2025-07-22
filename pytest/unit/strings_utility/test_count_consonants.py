import pytest
from strings_utility.count_consonants import count_consonants

def test_mixed_case_consonants_and_vowels() -> None:
    """
    Test the count_consonants function with mixed case consonants and vowels.
    """
    # Test case 1: String with mixed case consonants and vowels
    assert count_consonants("hello") == 3, "Failed on mixed case consonants and vowels"
    # Test case 2: String with mixed case consonants
    assert count_consonants("HeLLo WoRLd") == 7, "Failed on mixed case consonants"

def test_all_consonants() -> None:
    """
    Test the count_consonants function with all consonants.
    """
    # Test case 3: String with all consonants
    assert count_consonants("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ") == 42, "Failed on all consonants"
    # Test case 4: String with only consonants
    assert count_consonants("bcdfghjklmnpqrstvwxyz") == 21, "Failed on string with only consonants"
    # Test case 5: String with only uppercase consonants
    assert count_consonants("BCDFGHJKLMNPQRSTVWXYZ") == 21, "Failed on string with only uppercase consonants"
    # Test case 6: String with repeated consonants
    assert count_consonants("bbccddffgghhjjkkllmmnnppqqrrssttvvwwxxyyzz") == 42, "Failed on string with repeated consonants"

def test_all_vowels() -> None:
    """
    Test the count_consonants function with all vowels.
    """
    # Test case 7: String with all vowels
    assert count_consonants("aeiouAEIOU") == 0, "Failed on all vowels"

def test_empty_string() -> None:
    """
    Test the count_consonants function with an empty string.
    """
    # Test case 8: Empty string
    assert count_consonants("") == 0, "Failed on empty string"

def test_numbers_and_special_characters() -> None:
    """
    Test the count_consonants function with numbers and special characters.
    """
    # Test case 9: String with numbers and special characters
    assert count_consonants("12345!@#$%") == 0, "Failed on string with numbers and special characters"
    # Test case 10: String with mixed consonants, vowels, numbers, and special characters
    assert count_consonants("h3ll0 w0rld!") == 7, "Failed on mixed consonants, vowels, numbers, and special characters"
    # Test case 11: String with punctuation
    assert count_consonants("hello, world!") == 7, "Failed on string with punctuation"
    # Test case 12: String with special characters
    assert count_consonants("!@#hello!@#") == 3, "Failed on string with special characters"
    # Test case 13: String with numbers
    assert count_consonants("123hello123") == 3, "Failed on string with numbers"

def test_whitespace_characters() -> None:
    """
    Test the count_consonants function with whitespace characters.
    """
    # Test case 14: String with spaces
    assert count_consonants("hello world") == 7, "Failed on string with spaces"
    # Test case 15: String with newline characters
    assert count_consonants("hello\nworld") == 7, "Failed on string with newline characters"
    # Test case 16: String with tab characters
    assert count_consonants("hello\tworld") == 7, "Failed on string with tab characters"
    # Test case 17: String with mixed whitespace characters
    assert count_consonants("hello \t\nworld") == 7, "Failed on string with mixed whitespace characters"
    # Test case 18: String with leading and trailing spaces
    assert count_consonants("  hello world  ") == 7, "Failed on string with leading and trailing spaces"

def test_non_english_characters() -> None:
    """
    Test the count_consonants function with non-English characters.
    """
    # Test case 19: String with non-English characters
    assert count_consonants("héllo wörld") == 7, "Failed on string with non-English characters"

def test_count_consonants_invalid_type() -> None:
    """
    Test the count_consonants function with an invalid type.
    """
    # Test case 20: Invalid type
    with pytest.raises(TypeError):
        count_consonants(12345)

