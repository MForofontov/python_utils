import pytest
from strings_utility.center_string import center_string


def test_center_string_default_fill() -> None:
    """
    Test case 1: Test the center_string function with the default fill character (space).
    """
    assert (
        center_string("hello", 11) == "   hello   "
    ), "Failed on default fill character"


def test_center_string_custom_fill() -> None:
    """
    Test case 2: Test the center_string function with a custom fill character.
    """
    assert (
        center_string("hello", 11, "-") == "---hello---"
    ), "Failed on custom fill character"


def test_center_string_width_less_than_length() -> None:
    """
    Test case 3: Test the center_string function with width less than string length.
    """
    assert (
        center_string("hello", 3) == "hello"
    ), "Failed on width less than string length"


def test_center_string_width_equal_to_length() -> None:
    """
    Test case 4: Test the center_string function with width equal to string length.
    """
    assert (
        center_string("hello", 5) == "hello"
    ), "Failed on width equal to string length"


def test_center_string_empty_string() -> None:
    """
    Test case 5: Test the center_string function with an empty string.
    """
    assert center_string("", 5) == "     ", "Failed on empty string"


def test_center_string_zero_width() -> None:
    """
    Test case 6: Test the center_string function with width of zero.
    """
    assert center_string("hello", 0) == "hello", "Failed on width of zero"


def test_center_string_negative_width() -> None:
    """
    Test case 7: Test the center_string function with width of negative value.
    """
    assert center_string("hello", -5) == "hello", "Failed on negative width"


def test_center_string_even_width() -> None:
    """
    Test case 8: Test the center_string function with even width.
    """
    assert center_string("hello", 10) == "  hello   ", "Failed on even width"


def test_center_string_odd_width() -> None:
    """
    Test case 9: Test the center_string function with odd width.
    """
    assert center_string("hello", 9) == "  hello  ", "Failed on odd width"


def test_center_string_multiple_custom_fill() -> None:
    """
    Test case 10: Test the center_string function with multiple custom fill characters.
    """
    assert (
        center_string("hello", 11, "*") == "***hello***"
    ), "Failed on multiple custom fill characters"


def test_center_string_single_character() -> None:
    """
    Test case 11: Test the center_string function with a single character.
    """
    assert center_string("h", 5) == "  h  ", "Failed on single character"


def test_center_string_special_characters() -> None:
    """
    Test case 12: Test the center_string function with special characters.
    """
    assert center_string("!@#", 7) == "  !@#  ", "Failed on special characters"


def test_center_string_numbers() -> None:
    """
    Test case 13: Test the center_string function with numbers.
    """
    assert center_string("12345", 10) == "  12345   ", "Failed on numbers"


def test_center_string_mixed_characters() -> None:
    """
    Test case 14: Test the center_string function with mixed characters.
    """
    assert center_string(
        "a1!b2@", 12) == "   a1!b2@   ", "Failed on mixed characters"


def test_center_string_leading_trailing_spaces() -> None:
    """
    Test case 15: Test the center_string function with leading and trailing spaces.
    """
    assert (
        center_string("  hello  ", 15) == "     hello     "
    ), "Failed on leading and trailing spaces"


def test_center_string_newline_characters() -> None:
    """
    Test case 16: Test the center_string function with newline characters.
    """
    assert (
        center_string("hello\nworld", 15) == "  hello\nworld  "
    ), "Failed on newline characters"


def test_center_string_tab_characters() -> None:
    """
    Test case 17: Test the center_string function with tab characters.
    """
    assert (
        center_string("hello\tworld", 15) == "  hello\tworld  "
    ), "Failed on tab characters"


def test_center_string_mixed_whitespace_characters() -> None:
    """
    Test case 18: Test the center_string function with mixed whitespace characters.
    """
    assert (
        center_string("hello \t\nworld", 20) == "   hello \t\nworld    "
    ), "Failed on mixed whitespace characters"


def test_center_string_non_english_characters() -> None:
    """
    Test case 19: Test the center_string function with non-English characters.
    """
    assert (
        center_string("héllo wörld", 15) == "  héllo wörld  "
    ), "Failed on non-English characters"


def test_center_string_invalid_string_type() -> None:
    """
    Test case 20: Test the center_string function with an invalid string type.
    """
    with pytest.raises(TypeError):
        center_string(12345, 15)


def test_center_string_invalid_width_type() -> None:
    """
    Test case 21: Test the center_string function with an invalid width type.
    """
    with pytest.raises(TypeError):
        center_string("hello world", "15")


def test_center_string_invalid_fillchar_type() -> None:
    """
    Test case 22: Test the center_string function with an invalid fill character type.
    """
    with pytest.raises(TypeError):
        center_string("hello world", 15, 5)


def test_center_string_invalid_fillchar_length() -> None:
    """
    Test case 23: Test the center_string function with an invalid fill character length.
    """
    with pytest.raises(TypeError):
        center_string("hello world", 15, "ab")
