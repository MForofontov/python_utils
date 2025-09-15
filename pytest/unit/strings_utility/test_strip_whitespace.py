import pytest
from strings_utility.strip_whitespace import strip_whitespace


def test_strip_whitespace_basic() -> None:
    """
    Test case 1: Test the strip_whitespace function with a basic string containing leading and trailing spaces.
    """
    assert strip_whitespace("  hello  ") == "hello", (
        "Failed on basic string with leading and trailing spaces"
    )


def test_strip_whitespace_no_whitespace() -> None:
    """
    Test case 2: Test the strip_whitespace function with a string that has no leading or trailing whitespace.
    """
    assert strip_whitespace("hello") == "hello", (
        "Failed on string with no leading or trailing whitespace"
    )


def test_strip_whitespace_only_whitespace() -> None:
    """
    Test case 3: Test the strip_whitespace function with a string that contains only whitespace.
    """
    assert strip_whitespace("     ") == "", "Failed on string with only whitespace"


def test_strip_whitespace_empty_string() -> None:
    """
    Test case 4: Test the strip_whitespace function with an empty string.
    """
    assert strip_whitespace("") == "", "Failed on empty string"


def test_strip_whitespace_leading_whitespace() -> None:
    """
    Test case 5: Test the strip_whitespace function with a string that has leading whitespace.
    """
    assert strip_whitespace("   hello") == "hello", (
        "Failed on string with leading whitespace"
    )


def test_strip_whitespace_trailing_whitespace() -> None:
    """
    Test case 6: Test the strip_whitespace function with a string that has trailing whitespace.
    """
    assert strip_whitespace("hello   ") == "hello", (
        "Failed on string with trailing whitespace"
    )


def test_strip_whitespace_mixed_whitespace() -> None:
    """
    Test case 7: Test the strip_whitespace function with a string that has mixed whitespace characters.
    """
    assert strip_whitespace(" \t\nhello \t\n") == "hello", (
        "Failed on string with mixed whitespace characters"
    )


def test_strip_whitespace_special_characters() -> None:
    """
    Test case 8: Test the strip_whitespace function with a string that contains special characters.
    """
    assert strip_whitespace("  !@#  ") == "!@#", (
        "Failed on string with special characters"
    )


def test_strip_whitespace_numbers() -> None:
    """
    Test case 9: Test the strip_whitespace function with a string that contains numbers.
    """
    assert strip_whitespace("  12345  ") == "12345", "Failed on string with numbers"


def test_strip_whitespace_mixed_case() -> None:
    """
    Test case 10: Test the strip_whitespace function with a string that contains mixed case letters.
    """
    assert strip_whitespace("  HelloWorld  ") == "HelloWorld", (
        "Failed on string with mixed case letters"
    )


def test_strip_whitespace_non_english_characters() -> None:
    """
    Test case 11: Test the strip_whitespace function with a string that contains non-English characters.
    """
    assert strip_whitespace("  héllo wörld  ") == "héllo wörld", (
        "Failed on string with non-English characters"
    )


def test_strip_whitespace_invalid_type() -> None:
    """
    Test case 12: Test the strip_whitespace function with an invalid type.
    """
    with pytest.raises(TypeError):
        strip_whitespace(12345)
