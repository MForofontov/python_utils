import pytest
from strings_utility.to_lowercase import to_lowercase


def test_to_lowercase_basic() -> None:
    """
    Test the to_lowercase function with a basic uppercase string.
    """
    # Test case 1: Basic uppercase string
    assert to_lowercase("HELLO") == "hello", "Failed on basic uppercase string"


def test_to_lowercase_mixed_case() -> None:
    """
    Test the to_lowercase function with a mixed case string.
    """
    # Test case 2: Mixed case string
    assert to_lowercase(
        "HeLLo WoRLd") == "hello world", "Failed on mixed case string"


def test_to_lowercase_all_lowercase() -> None:
    """
    Test the to_lowercase function with an all lowercase string.
    """
    # Test case 3: All lowercase string
    assert to_lowercase("hello") == "hello", "Failed on all lowercase string"


def test_to_lowercase_numbers() -> None:
    """
    Test the to_lowercase function with a string that contains numbers.
    """
    # Test case 4: String with numbers
    assert to_lowercase(
        "Hello123") == "hello123", "Failed on string with numbers"


def test_to_lowercase_special_characters() -> None:
    """
    Test the to_lowercase function with a string that contains special characters.
    """
    # Test case 5: String with special characters
    assert (
        to_lowercase("Hello!@#") == "hello!@#"
    ), "Failed on string with special characters"


def test_to_lowercase_whitespace() -> None:
    """
    Test the to_lowercase function with a string that contains whitespace.
    """
    # Test case 6: String with whitespace
    assert (
        to_lowercase(" Hello World ") == " hello world "
    ), "Failed on string with whitespace"


def test_to_lowercase_empty_string() -> None:
    """
    Test the to_lowercase function with an empty string.
    """
    # Test case 7: Empty string
    assert to_lowercase("") == "", "Failed on empty string"


def test_to_lowercase_non_english_characters() -> None:
    """
    Test the to_lowercase function with a string that contains non-English characters.
    """
    # Test case 8: String with non-English characters
    assert (
        to_lowercase("HÉLLO WÖRLD") == "héllo wörld"
    ), "Failed on string with non-English characters"


def test_to_lowercase_mixed_whitespace() -> None:
    """
    Test the to_lowercase function with a string that contains mixed whitespace characters.
    """
    # Test case 9: String with mixed whitespace characters
    assert (
        to_lowercase(" \t\nHello World\t\n ") == " \t\nhello world\t\n "
    ), "Failed on string with mixed whitespace characters"


def test_to_lowercase_invalid_type() -> None:
    """
    Test the to_lowercase function with an invalid type.
    """
    # Test case 10: Invalid type
    with pytest.raises(TypeError):
        to_lowercase(12345)
