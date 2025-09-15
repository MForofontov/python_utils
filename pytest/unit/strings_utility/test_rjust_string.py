import pytest
from strings_utility.rjust_string import rjust_string


def test_rjust_string_default_fill() -> None:
    """
    Test case 1: Test the rjust_string function with the default fill character (space).
    """
    assert rjust_string("hello", 10) == "     hello", "Failed on default fill character"


def test_rjust_string_custom_fill() -> None:
    """
    Test case 2: Test the rjust_string function with a custom fill character.
    """
    assert (
        rjust_string("hello", 10, "-") == "-----hello"
    ), "Failed on custom fill character"


def test_rjust_string_width_less_than_length() -> None:
    """
    Test case 3: Test the rjust_string function with width less than string length.
    """
    assert (
        rjust_string("hello", 3) == "hello"
    ), "Failed on width less than string length"


def test_rjust_string_width_equal_to_length() -> None:
    """
    Test case 4: Test the rjust_string function with width equal to string length.
    """
    assert rjust_string("hello", 5) == "hello", "Failed on width equal to string length"


def test_rjust_string_empty_string() -> None:
    """
    Test case 5: Test the rjust_string function with an empty string.
    """
    assert rjust_string("", 5) == "     ", "Failed on empty string"


def test_rjust_string_zero_width() -> None:
    """
    Test case 6: Test the rjust_string function with width of zero.
    """
    assert rjust_string("hello", 0) == "hello", "Failed on width of zero"


def test_rjust_string_special_characters() -> None:
    """
    Test case 7: Test the rjust_string function with a string that contains special characters.
    """
    assert (
        rjust_string("!@#", 5, "-") == "--!@#"
    ), "Failed on string with special characters"


def test_rjust_string_numbers() -> None:
    """
    Test case 8: Test the rjust_string function with a string that contains numbers.
    """
    assert rjust_string("123", 5, "0") == "00123", "Failed on string with numbers"


def test_rjust_string_mixed_case() -> None:
    """
    Test case 9: Test the rjust_string function with a string that contains mixed case letters.
    """
    assert (
        rjust_string("AbC", 5, "_") == "__AbC"
    ), "Failed on string with mixed case letters"


def test_rjust_string_non_english_characters() -> None:
    """
    Test case 10: Test the rjust_string function with a string that contains non-English characters.
    """
    assert (
        rjust_string("héllo", 8, "*") == "***héllo"
    ), "Failed on string with non-English characters"


def test_rjust_string_invalid_string_type() -> None:
    """
    Test case 11: Test the rjust_string function with an invalid string type.
    """
    with pytest.raises(TypeError):
        rjust_string(12345, 10)


def test_rjust_string_invalid_width_type() -> None:
    """
    Test case 12: Test the rjust_string function with an invalid width type.
    """
    with pytest.raises(TypeError):
        rjust_string("hello", "10")


def test_rjust_string_invalid_fillchar_type() -> None:
    """
    Test case 13: Test the rjust_string function with an invalid fill character type.
    """
    with pytest.raises(TypeError):
        rjust_string("hello", 10, 5)


def test_rjust_string_invalid_fillchar_length() -> None:
    """
    Test case 14: Test the rjust_string function with an invalid fill character length.
    """
    with pytest.raises(TypeError):
        rjust_string("hello", 10, "--")
