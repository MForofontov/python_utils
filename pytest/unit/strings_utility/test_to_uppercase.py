import pytest
from strings_utility.to_uppercase import to_uppercase


def test_to_uppercase_basic() -> None:
    """
    Test the to_uppercase function with a basic lowercase string.
    """
    # Test case 1: Basic lowercase string
    assert to_uppercase("hello") == "HELLO", "Failed on basic lowercase string"


def test_to_uppercase_mixed_case() -> None:
    """
    Test the to_uppercase function with a mixed case string.
    """
    # Test case 2: Mixed case string
    assert to_uppercase("HeLLo WoRLd") == "HELLO WORLD", "Failed on mixed case string"


def test_to_uppercase_all_uppercase() -> None:
    """
    Test the to_uppercase function with an all uppercase string.
    """
    # Test case 3: All uppercase string
    assert to_uppercase("HELLO") == "HELLO", "Failed on all uppercase string"


def test_to_uppercase_numbers() -> None:
    """
    Test the to_uppercase function with a string that contains numbers.
    """
    # Test case 4: String with numbers
    assert to_uppercase("Hello123") == "HELLO123", "Failed on string with numbers"


def test_to_uppercase_special_characters() -> None:
    """
    Test the to_uppercase function with a string that contains special characters.
    """
    # Test case 5: String with special characters
    assert (
        to_uppercase("Hello!@#") == "HELLO!@#"
    ), "Failed on string with special characters"


def test_to_uppercase_whitespace() -> None:
    """
    Test the to_uppercase function with a string that contains whitespace.
    """
    # Test case 6: String with whitespace
    assert (
        to_uppercase(" Hello World ") == " HELLO WORLD "
    ), "Failed on string with whitespace"


def test_to_uppercase_empty_string() -> None:
    """
    Test the to_uppercase function with an empty string.
    """
    # Test case 7: Empty string
    assert to_uppercase("") == "", "Failed on empty string"


def test_to_uppercase_non_english_characters() -> None:
    """
    Test the to_uppercase function with a string that contains non-English characters.
    """
    # Test case 8: String with non-English characters
    assert (
        to_uppercase("héllo wörld") == "HÉLLO WÖRLD"
    ), "Failed on string with non-English characters"


def test_to_uppercase_mixed_whitespace() -> None:
    """
    Test the to_uppercase function with a string that contains mixed whitespace characters.
    """
    # Test case 9: String with mixed whitespace characters
    assert (
        to_uppercase(" \t\nHello World\t\n ") == " \t\nHELLO WORLD\t\n "
    ), "Failed on string with mixed whitespace characters"


def test_to_uppercase_invalid_type() -> None:
    """
    Test the to_uppercase function with an invalid type.
    """
    # Test case 10: Invalid type
    with pytest.raises(TypeError):
        to_uppercase(12345)
