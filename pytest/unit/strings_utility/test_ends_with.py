import pytest
from strings_utility.ends_with import ends_with


def test_string_ends_with_suffix() -> None:
    """
    Test if the string ends with the specified suffix.
    """
    # Test case 1: String ends with the suffix
    assert (
        ends_with("hello world", "world") == True
    ), "Failed on string ending with suffix"


def test_string_does_not_end_with_suffix() -> None:
    """
    Test if the string does not end with the specified suffix.
    """
    # Test case 2: String does not end with the suffix
    assert (
        ends_with("hello world", "hello") == False
    ), "Failed on string not ending with suffix"


def test_suffix_is_entire_string() -> None:
    """
    Test if the suffix is the entire string.
    """
    # Test case 3: Suffix is the entire string
    assert (
        ends_with("hello", "hello") == True
    ), "Failed on suffix being the entire string"


def test_empty_suffix() -> None:
    """
    Test if the suffix is empty.
    """
    # Test case 4: Empty suffix
    assert ends_with("hello", "") == True, "Failed on empty suffix"


def test_empty_string_and_non_empty_suffix() -> None:
    """
    Test if the string is empty and the suffix is non-empty.
    """
    # Test case 5: Empty string and non-empty suffix
    assert (
        ends_with("", "hello") == False
    ), "Failed on empty string and non-empty suffix"


def test_both_string_and_suffix_are_empty() -> None:
    """
    Test if both the string and the suffix are empty.
    """
    # Test case 6: Both string and suffix are empty
    assert ends_with(
        "", "") == True, "Failed on both string and suffix being empty"


def test_suffix_longer_than_string() -> None:
    """
    Test if the suffix is longer than the string.
    """
    # Test case 7: Suffix longer than string
    assert (
        ends_with("hello", "hello world") == False
    ), "Failed on suffix longer than string"


def test_string_ends_with_special_characters() -> None:
    """
    Test if the string ends with special characters.
    """
    # Test case 8: String ends with special characters
    assert (
        ends_with("hello!@#", "!@#") == True
    ), "Failed on string ending with special characters"


def test_string_does_not_end_with_special_characters() -> None:
    """
    Test if the string does not end with special characters.
    """
    # Test case 9: String does not end with special characters
    assert (
        ends_with("hello!@#", "@!") == False
    ), "Failed on string not ending with special characters"


def test_string_ends_with_space() -> None:
    """
    Test if the string ends with a space.
    """
    # Test case 10: String ends with a space
    assert (
        ends_with("hello world ", " ") == True
    ), "Failed on string ending with a space"


def test_string_does_not_end_with_space() -> None:
    """
    Test if the string does not end with a space.
    """
    # Test case 11: String does not end with a space
    assert (
        ends_with("hello world", " ") == False
    ), "Failed on string not ending with a space"


def test_string_ends_with_newline_character() -> None:
    """
    Test if the string ends with a newline character.
    """
    # Test case 12: String ends with a newline character
    assert (
        ends_with("hello world\n", "\n") == True
    ), "Failed on string ending with a newline character"


def test_string_does_not_end_with_newline_character() -> None:
    """
    Test if the string does not end with a newline character.
    """
    # Test case 13: String does not end with a newline character
    assert (
        ends_with("hello world", "\n") == False
    ), "Failed on string not ending with a newline character"


def test_string_ends_with_tab_character() -> None:
    """
    Test if the string ends with a tab character.
    """
    # Test case 14: String ends with a tab character
    assert (
        ends_with("hello world\t", "\t") == True
    ), "Failed on string ending with a tab character"


def test_string_does_not_end_with_tab_character() -> None:
    """
    Test if the string does not end with a tab character.
    """
    # Test case 15: String does not end with a tab character
    assert (
        ends_with("hello world", "\t") == False
    ), "Failed on string not ending with a tab character"


def test_string_ends_with_digit() -> None:
    """
    Test if the string ends with a digit.
    """
    # Test case 16: String ends with a digit
    assert (
        ends_with("hello world 123", "123") == True
    ), "Failed on string ending with a digit"


def test_string_does_not_end_with_digit() -> None:
    """
    Test if the string does not end with a digit.
    """
    # Test case 17: String does not end with a digit
    assert (
        ends_with("hello world 123", "124") == False
    ), "Failed on string not ending with a digit"


def test_string_ends_with_mixed_case_suffix() -> None:
    """
    Test if the string ends with a mixed case suffix.
    """
    # Test case 18: String ends with mixed case suffix
    assert (
        ends_with("hello world", "World") == False
    ), "Failed on string ending with mixed case suffix"


def test_string_ends_with_mixed_case_suffix_case_insensitive() -> None:
    """
    Test if the string ends with a mixed case suffix (case insensitive).
    """
    # Test case 19: String ends with mixed case suffix (case insensitive)
    assert (
        ends_with("hello world", "World".lower()) == True
    ), "Failed on string ending with mixed case suffix (case insensitive)"


def test_string_ends_with_non_english_characters() -> None:
    """
    Test if the string ends with non-English characters.
    """
    # Test case 20: String ends with non-English characters
    assert (
        ends_with("héllo wörld", "wörld") == True
    ), "Failed on string ending with non-English characters"


def test_ends_with_invalid_string_type() -> None:
    """
    Test the ends_with function with an invalid string type.
    """
    # Test case 21: Invalid string type
    with pytest.raises(TypeError):
        ends_with(12345, "world")


def test_ends_with_invalid_suffix_type() -> None:
    """
    Test the ends_with function with an invalid suffix type.
    """
    # Test case 22: Invalid suffix type
    with pytest.raises(TypeError):
        ends_with("hello world", 123)
