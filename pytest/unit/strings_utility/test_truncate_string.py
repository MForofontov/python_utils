import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from strings_utility.truncate_string import truncate_string


def test_truncate_string_basic() -> None:
    """
    Test case 1: Test the truncate_string function with basic truncation.
    """
    assert truncate_string("hello world", 5) == "hello", "Failed on basic truncation"


def test_truncate_string_length_greater_than_string() -> None:
    """
    Test case 2: Test the truncate_string function with length greater than the string length.
    """
    assert truncate_string("abc", 5) == "abc", (
        "Failed on length greater than the string length"
    )


def test_truncate_string_length_equal_to_string() -> None:
    """
    Test case 3: Test the truncate_string function with length equal to the string length.
    """
    assert truncate_string("hello", 5) == "hello", (
        "Failed on length equal to the string length"
    )


def test_truncate_string_length_zero() -> None:
    """
    Test case 4: Test the truncate_string function with length zero.
    """
    assert truncate_string("hello", 0) == "", "Failed on length zero"


def test_truncate_string_empty_string() -> None:
    """
    Test case 5: Test the truncate_string function with an empty string.
    """
    assert truncate_string("", 5) == "", "Failed on empty string"


def test_truncate_string_special_characters() -> None:
    """
    Test case 6: Test the truncate_string function with a string that contains special characters.
    """
    assert truncate_string("!@#hello$%^", 3) == "!@#", (
        "Failed on string with special characters"
    )


def test_truncate_string_numbers() -> None:
    """
    Test case 7: Test the truncate_string function with a string that contains numbers.
    """
    assert truncate_string("1234567890", 5) == "12345", "Failed on string with numbers"


def test_truncate_string_mixed_case() -> None:
    """
    Test case 8: Test the truncate_string function with a string that contains mixed case letters.
    """
    assert truncate_string("HeLLoWoRLd", 7) == "HeLLoWo", (
        "Failed on string with mixed case letters"
    )


def test_truncate_string_non_english_characters() -> None:
    """
    Test case 9: Test the truncate_string function with a string that contains non-English characters.
    """
    assert truncate_string("héllo wörld", 5) == "héllo", (
        "Failed on string with non-English characters"
    )


def test_truncate_string_mixed_whitespace() -> None:
    """
    Test case 10: Test the truncate_string function with a string that contains mixed whitespace characters.
    """
    assert truncate_string(" \t\nhello world\t\n ", 8) == " \t\nhello", (
        "Failed on string with mixed whitespace characters"
    )


def test_truncate_string_negative_length() -> None:
    """
    Test case 11: Test the truncate_string function with a negative length.
    """
    with pytest.raises(ValueError, match="length must be non-negative"):
        truncate_string("hello", -3)


def test_truncate_string_invalid_string_type() -> None:
    """
    Test case 12: Test the truncate_string function with an invalid string type.
    """
    with pytest.raises(TypeError):
        truncate_string(12345, 3)


def test_truncate_string_invalid_length_type() -> None:
    """
    Test case 13: Test the truncate_string function with an invalid length type.
    """
    with pytest.raises(TypeError):
        truncate_string("hello", "3")
