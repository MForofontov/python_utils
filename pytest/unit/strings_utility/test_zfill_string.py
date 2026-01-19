import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from strings_utility.zfill_string import zfill_string


def test_zfill_string_basic() -> None:
    """
    Test case 1: Test the zfill_string function with a basic numeric string.
    """
    assert zfill_string("42", 5) == "00042", "Failed on basic numeric string"


def test_zfill_string_negative_number() -> None:
    """
    Test case 2: Test the zfill_string function with a negative numeric string.
    """
    assert zfill_string("-42", 5) == "-0042", "Failed on negative numeric string"


def test_zfill_string_length_equal_to_width() -> None:
    """
    Test case 3: Test the zfill_string function with a string length equal to the specified width.
    """
    assert zfill_string("12345", 5) == "12345", (
        "Failed on string length equal to the specified width"
    )


def test_zfill_string_length_greater_than_width() -> None:
    """
    Test case 4: Test the zfill_string function with a string length greater than the specified width.
    """
    assert zfill_string("123456", 5) == "123456", (
        "Failed on string length greater than the specified width"
    )


def test_zfill_string_empty_string() -> None:
    """
    Test case 5: Test the zfill_string function with an empty string.
    """
    assert zfill_string("", 5) == "00000", "Failed on empty string"


def test_zfill_string_special_characters() -> None:
    """
    Test case 6: Test the zfill_string function with a string that contains special characters.
    """
    assert zfill_string("!@#", 5) == "00!@#", "Failed on string with special characters"


def test_zfill_string_numbers_and_letters() -> None:
    """
    Test case 7: Test the zfill_string function with a string that contains both numbers and letters.
    """
    assert zfill_string("abc123", 8) == "00abc123", (
        "Failed on string with numbers and letters"
    )


def test_zfill_string_non_english_characters() -> None:
    """
    Test case 8: Test the zfill_string function with a string that contains non-English characters.
    """
    assert zfill_string("héllo", 7) == "00héllo", (
        "Failed on string with non-English characters"
    )


def test_zfill_string_mixed_whitespace() -> None:
    """
    Test case 9: Test the zfill_string function with a string that contains mixed whitespace characters.
    """
    assert zfill_string(" \t\n42", 6) == "0 \t\n42", (
        "Failed on string with mixed whitespace characters"
    )


def test_zfill_string_invalid_string_type() -> None:
    """
    Test case 10: Test the zfill_string function with an invalid string type.
    """
    with pytest.raises(TypeError):
        zfill_string(12345, 5)


def test_zfill_string_invalid_width_type() -> None:
    """
    Test case 11: Test the zfill_string function with an invalid width type.
    """
    with pytest.raises(TypeError):
        zfill_string("42", "5")


def test_zfill_string_negative_width() -> None:
    """
    Test case 12: Test ValueError when width is negative.
    """
    with pytest.raises(ValueError, match="The width must be non-negative"):
        zfill_string("42", -5)
