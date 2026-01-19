import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from python_utils.strings_utility.is_anagram import is_anagram


def test_is_anagram_basic() -> None:
    """
    Test case 1: Test the is_anagram function with basic input.
    """
    assert is_anagram("listen", "silent"), "Failed on basic anagram"


def test_is_anagram_with_spaces() -> None:
    """
    Test case 2: Test the is_anagram function with strings containing spaces.
    """
    assert is_anagram("conversation", "voices rant on"), "Failed on anagram with spaces"


def test_is_anagram_with_different_cases() -> None:
    """
    Test case 3: Test the is_anagram function with strings containing different cases.
    """
    assert is_anagram("Listen", "Silent"), "Failed on anagram with different cases"


def test_is_anagram_with_non_anagram() -> None:
    """
    Test case 4: Test the is_anagram function with non-anagram strings.
    """
    assert not is_anagram("hello", "world"), "Failed on non-anagram strings"


def test_is_anagram_with_empty_strings() -> None:
    """
    Test case 5: Test the is_anagram function with empty strings.
    """
    assert is_anagram("", ""), "Failed on empty strings"


def test_is_anagram_with_special_characters() -> None:
    """
    Test case 6: Test the is_anagram function with strings containing special characters.
    """
    assert is_anagram("a!b@c#", "c@b!a#"), "Failed on anagram with special characters"


def test_is_anagram_with_numbers() -> None:
    """
    Test case 7: Test the is_anagram function with strings containing numbers.
    """
    assert is_anagram("12345", "54321"), "Failed on anagram with numbers"


def test_is_anagram_with_unicode_characters() -> None:
    """
    Test case 8: Test the is_anagram function with strings containing unicode characters.
    """
    assert is_anagram("déjà vu", "vu déjà"), "Failed on anagram with unicode characters"


def test_is_anagram_invalid_string_1_type() -> None:
    """
    Test case 9: Test the is_anagram function with an invalid type for the first string.
    """
    with pytest.raises(TypeError):
        is_anagram(123, "silent")  # type: ignore


def test_is_anagram_invalid_string_2_type() -> None:
    """
    Test case 10: Test the is_anagram function with an invalid type for the second string.
    """
    with pytest.raises(TypeError):
        is_anagram("listen", 123)  # type: ignore
