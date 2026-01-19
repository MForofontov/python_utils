import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from strings_utility.count_vowels import count_vowels


@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello", 2),
        ("HeLLo WoRLd", 3),
        ("aEiOuBcDfGh", 5),
    ],
)
def test_mixed_case_vowels_and_consonants(text: str, expected: int) -> None:
    """
    Test case 1: Mixed case vowels and consonants.
    """
    assert count_vowels(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("aeiouAEIOU", 10),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("aaaeeeiiiooouuu", 15),
    ],
)
def test_all_vowels(text: str, expected: int) -> None:
    """
    Test case 2: All vowels.
    """
    assert count_vowels(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ",
        "bcdfghjklmnpqrstvwxyz",
    ],
)
def test_all_consonants(text: str) -> None:
    """
    Test case 3: All consonants.
    """
    assert count_vowels(text) == 0


def test_empty_string() -> None:
    """
    Test case 4: Empty string.
    """
    assert count_vowels("") == 0


@pytest.mark.parametrize(
    "text, expected",
    [
        ("12345!@#$%", 0),
        ("h3llo w0rld!", 1),
        ("hello, world!", 3),
        ("!@#hello!@#", 2),
        ("123hello123", 2),
    ],
)
def test_numbers_and_special_characters(text: str, expected: int) -> None:
    """
    Test case 5: Numbers and special characters.
    """
    assert count_vowels(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello world", 3),
        ("hello\nworld", 3),
        ("hello\tworld", 3),
        ("hello \t\nworld", 3),
        ("  hello world  ", 3),
    ],
)
def test_whitespace_characters(text: str, expected: int) -> None:
    """
    Test case 6: Whitespace characters.
    """
    assert count_vowels(text) == expected


def test_non_english_characters() -> None:
    """
    Test case 7: Non english characters.
    """
    assert count_vowels("héllo wörld") == 1


def test_count_vowels_invalid_type() -> None:
    """
    Test case 8: Count vowels invalid type.
    """
    with pytest.raises(TypeError):
        count_vowels(12345)
