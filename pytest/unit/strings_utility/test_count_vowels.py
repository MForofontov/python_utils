import pytest
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
    assert count_vowels(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ",
        "bcdfghjklmnpqrstvwxyz",
    ],
)
def test_all_consonants(text: str) -> None:
    assert count_vowels(text) == 0


def test_empty_string() -> None:
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
    assert count_vowels(text) == expected


def test_non_english_characters() -> None:
    assert count_vowels("héllo wörld") == 1


def test_count_vowels_invalid_type() -> None:
    with pytest.raises(TypeError):
        count_vowels(12345)

