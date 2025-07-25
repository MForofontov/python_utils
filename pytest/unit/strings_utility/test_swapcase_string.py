import pytest
from strings_utility.swapcase_string import swapcase_string


def test_swapcase_string_basic() -> None:
    """
    Test the swapcase_string function with a basic string.
    """
    # Test case 1: Basic string
    assert swapcase_string("Hello World") == "hELLO wORLD", "Failed on basic string"


def test_swapcase_string_all_lowercase() -> None:
    """
    Test the swapcase_string function with an all lowercase string.
    """
    # Test case 2: All lowercase string
    assert swapcase_string("python") == "PYTHON", "Failed on all lowercase string"


def test_swapcase_string_all_uppercase() -> None:
    """
    Test the swapcase_string function with an all uppercase string.
    """
    # Test case 3: All uppercase string
    assert swapcase_string("PYTHON") == "python", "Failed on all uppercase string"


def test_swapcase_string_mixed_case() -> None:
    """
    Test the swapcase_string function with a mixed case string.
    """
    # Test case 4: Mixed case string
    assert swapcase_string("PyThOn") == "pYtHoN", "Failed on mixed case string"


def test_swapcase_string_numbers() -> None:
    """
    Test the swapcase_string function with a string that contains numbers.
    """
    # Test case 5: String with numbers
    assert swapcase_string("Python123") == "pYTHON123", "Failed on string with numbers"


def test_swapcase_string_special_characters() -> None:
    """
    Test the swapcase_string function with a string that contains special characters.
    """
    # Test case 6: String with special characters
    assert (
        swapcase_string("Hello!@#") == "hELLO!@#"
    ), "Failed on string with special characters"


def test_swapcase_string_whitespace() -> None:
    """
    Test the swapcase_string function with a string that contains whitespace.
    """
    # Test case 7: String with whitespace
    assert (
        swapcase_string(" Hello World ") == " hELLO wORLD "
    ), "Failed on string with whitespace"


def test_swapcase_string_empty_string() -> None:
    """
    Test the swapcase_string function with an empty string.
    """
    # Test case 8: Empty string
    assert swapcase_string("") == "", "Failed on empty string"


def test_swapcase_string_non_english_characters() -> None:
    """
    Test the swapcase_string function with a string that contains non-English characters.
    """
    # Test case 9: String with non-English characters
    assert (
        swapcase_string("héllo wörld") == "HÉLLO WÖRLD"
    ), "Failed on string with non-English characters"


def test_swapcase_string_mixed_whitespace() -> None:
    """
    Test the swapcase_string function with a string that contains mixed whitespace characters.
    """
    # Test case 10: String with mixed whitespace characters
    assert (
        swapcase_string(" \t\nHello World\t\n ") == " \t\nhELLO wORLD\t\n "
    ), "Failed on string with mixed whitespace characters"


def test_swapcase_string_invalid_type() -> None:
    """
    Test the swapcase_string function with an invalid type.
    """
    # Test case 11: Invalid type
    with pytest.raises(TypeError):
        swapcase_string(12345)
