import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from python_utils.strings_utility.repeat_string import repeat_string


def test_repeat_string_multiple_times() -> None:
    """
    Test case 1: Test the repeat_string function with a string repeated multiple times.
    """
    assert repeat_string("hello", 3) == "hellohellohello", (
        "Failed on repeating string multiple times"
    )


def test_repeat_string_once() -> None:
    """
    Test case 2: Test the repeat_string function with a string repeated once.
    """
    assert repeat_string("hello", 1) == "hello", "Failed on repeating string once"


def test_repeat_string_zero_times() -> None:
    """
    Test case 3: Test the repeat_string function with a string repeated zero times.
    """
    assert repeat_string("hello", 0) == "", "Failed on repeating string zero times"


def test_repeat_string_empty_string() -> None:
    """
    Test case 4: Test the repeat_string function with an empty string.
    """
    assert repeat_string("", 5) == "", "Failed on repeating empty string"


def test_repeat_string_special_characters() -> None:
    """
    Test case 5: Test the repeat_string function with a string that contains special characters.
    """
    assert repeat_string("!@#", 3) == "!@#!@#!@#", (
        "Failed on repeating string with special characters"
    )


def test_repeat_string_numbers() -> None:
    """
    Test case 6: Test the repeat_string function with a string that contains numbers.
    """
    assert repeat_string("123", 2) == "123123", (
        "Failed on repeating string with numbers"
    )


def test_repeat_string_mixed_case() -> None:
    """
    Test case 7: Test the repeat_string function with a string that contains mixed case letters.
    """
    assert repeat_string("AbC", 2) == "AbCAbC", (
        "Failed on repeating string with mixed case letters"
    )


def test_repeat_string_whitespace_characters() -> None:
    """
    Test case 8: Test the repeat_string function with a string that contains whitespace characters.
    """
    assert repeat_string("a b", 3) == "a ba ba b", (
        "Failed on repeating string with whitespace characters"
    )


def test_repeat_string_newline_characters() -> None:
    """
    Test case 9: Test the repeat_string function with a string that contains newline characters.
    """
    assert repeat_string("a\nb", 2) == "a\nba\nb", (
        "Failed on repeating string with newline characters"
    )


def test_repeat_string_tab_characters() -> None:
    """
    Test case 10: Test the repeat_string function with a string that contains tab characters.
    """
    assert repeat_string("a\tb", 2) == "a\tba\tb", (
        "Failed on repeating string with tab characters"
    )


def test_repeat_string_mixed_whitespace_characters() -> None:
    """
    Test case 11: Test the repeat_string function with a string that contains mixed whitespace characters.
    """
    assert repeat_string("a \t\nb", 2) == "a \t\nba \t\nb", (
        "Failed on repeating string with mixed whitespace characters"
    )


def test_repeat_string_non_english_characters() -> None:
    """
    Test case 12: Test the repeat_string function with a string that contains non-English characters.
    """
    assert repeat_string("héllo", 2) == "héllohéllo", (
        "Failed on repeating string with non-English characters"
    )


def test_repeat_string_negative_times() -> None:
    """
    Test case 13: Test the repeat_string function with a string repeated negative times.
    """
    with pytest.raises(ValueError):
        repeat_string("hello", -1)


def test_repeat_string_invalid_string_type() -> None:
    """
    Test case 14: Test the repeat_string function with an invalid string type.
    """
    with pytest.raises(TypeError):
        repeat_string(123, 2)


def test_repeat_string_invalid_repeat_count_type() -> None:
    """
    Test case 15: Test the repeat_string function with an invalid repeat count type.
    """
    with pytest.raises(TypeError):
        repeat_string("hello", "2")
