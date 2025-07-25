import pytest
from strings_utility.repeat_string import repeat_string


def test_repeat_string_multiple_times() -> None:
    """
    Test the repeat_string function with a string repeated multiple times.
    """
    # Test case 1: Repeat a string multiple times
    assert (
        repeat_string("hello", 3) == "hellohellohello"
    ), "Failed on repeating string multiple times"


def test_repeat_string_once() -> None:
    """
    Test the repeat_string function with a string repeated once.
    """
    # Test case 2: Repeat a string once
    assert repeat_string("hello", 1) == "hello", "Failed on repeating string once"


def test_repeat_string_zero_times() -> None:
    """
    Test the repeat_string function with a string repeated zero times.
    """
    # Test case 3: Repeat a string zero times
    assert repeat_string("hello", 0) == "", "Failed on repeating string zero times"


def test_repeat_string_negative_times() -> None:
    """
    Test the repeat_string function with a string repeated negative times.
    """
    # Test case 4: Repeat a string negative times
    assert repeat_string("hello", -1) == "", "Failed on repeating string negative times"


def test_repeat_string_empty_string() -> None:
    """
    Test the repeat_string function with an empty string.
    """
    # Test case 5: Repeat an empty string
    assert repeat_string("", 5) == "", "Failed on repeating empty string"


def test_repeat_string_special_characters() -> None:
    """
    Test the repeat_string function with a string that contains special characters.
    """
    # Test case 6: Repeat a string with special characters
    assert (
        repeat_string("!@#", 3) == "!@#!@#!@#"
    ), "Failed on repeating string with special characters"


def test_repeat_string_numbers() -> None:
    """
    Test the repeat_string function with a string that contains numbers.
    """
    # Test case 7: Repeat a string with numbers
    assert (
        repeat_string("123", 2) == "123123"
    ), "Failed on repeating string with numbers"


def test_repeat_string_mixed_case() -> None:
    """
    Test the repeat_string function with a string that contains mixed case letters.
    """
    # Test case 8: Repeat a string with mixed case letters
    assert (
        repeat_string("AbC", 2) == "AbCAbC"
    ), "Failed on repeating string with mixed case letters"


def test_repeat_string_whitespace_characters() -> None:
    """
    Test the repeat_string function with a string that contains whitespace characters.
    """
    # Test case 9: Repeat a string with whitespace characters
    assert (
        repeat_string("a b", 3) == "a ba ba b"
    ), "Failed on repeating string with whitespace characters"


def test_repeat_string_newline_characters() -> None:
    """
    Test the repeat_string function with a string that contains newline characters.
    """
    # Test case 10: Repeat a string with newline characters
    assert (
        repeat_string("a\nb", 2) == "a\nba\nb"
    ), "Failed on repeating string with newline characters"


def test_repeat_string_tab_characters() -> None:
    """
    Test the repeat_string function with a string that contains tab characters.
    """
    # Test case 11: Repeat a string with tab characters
    assert (
        repeat_string("a\tb", 2) == "a\tba\tb"
    ), "Failed on repeating string with tab characters"


def test_repeat_string_mixed_whitespace_characters() -> None:
    """
    Test the repeat_string function with a string that contains mixed whitespace characters.
    """
    # Test case 12: Repeat a string with mixed whitespace characters
    assert (
        repeat_string("a \t\nb", 2) == "a \t\nba \t\nb"
    ), "Failed on repeating string with mixed whitespace characters"


def test_repeat_string_non_english_characters() -> None:
    """
    Test the repeat_string function with a string that contains non-English characters.
    """
    # Test case 13: Repeat a string with non-English characters
    assert (
        repeat_string("héllo", 2) == "héllohéllo"
    ), "Failed on repeating string with non-English characters"


def test_repeat_string_invalid_string_type() -> None:
    """
    Test the repeat_string function with an invalid string type.
    """
    # Test case 14: Invalid string type
    with pytest.raises(TypeError):
        repeat_string(123, 2)


def test_repeat_string_invalid_repeat_count_type() -> None:
    """
    Test the repeat_string function with an invalid repeat count type.
    """
    # Test case 15: Invalid repeat count type
    with pytest.raises(TypeError):
        repeat_string("hello", "2")
