import pytest

pytestmark = [pytest.mark.unit, pytest.mark.strings_utility]
from python_utils.strings_utility.swapcase_string import swapcase_string


def test_swapcase_string_basic() -> None:
    """
    Test case 1: Test the swapcase_string function with a basic string.
    """
    assert swapcase_string("Hello World") == "hELLO wORLD", "Failed on basic string"


def test_swapcase_string_all_lowercase() -> None:
    """
    Test case 2: Test the swapcase_string function with an all lowercase string.
    """
    assert swapcase_string("python") == "PYTHON", "Failed on all lowercase string"


def test_swapcase_string_all_uppercase() -> None:
    """
    Test case 3: Test the swapcase_string function with an all uppercase string.
    """
    assert swapcase_string("PYTHON") == "python", "Failed on all uppercase string"


def test_swapcase_string_mixed_case() -> None:
    """
    Test case 4: Test the swapcase_string function with a mixed case string.
    """
    assert swapcase_string("PyThOn") == "pYtHoN", "Failed on mixed case string"


def test_swapcase_string_numbers() -> None:
    """
    Test case 5: Test the swapcase_string function with a string that contains numbers.
    """
    assert swapcase_string("Python123") == "pYTHON123", "Failed on string with numbers"


def test_swapcase_string_special_characters() -> None:
    """
    Test case 6: Test the swapcase_string function with a string that contains special characters.
    """
    assert swapcase_string("Hello!@#") == "hELLO!@#", (
        "Failed on string with special characters"
    )


def test_swapcase_string_whitespace() -> None:
    """
    Test case 7: Test the swapcase_string function with a string that contains whitespace.
    """
    assert swapcase_string(" Hello World ") == " hELLO wORLD ", (
        "Failed on string with whitespace"
    )


def test_swapcase_string_empty_string() -> None:
    """
    Test case 8: Test the swapcase_string function with an empty string.
    """
    assert swapcase_string("") == "", "Failed on empty string"


def test_swapcase_string_non_english_characters() -> None:
    """
    Test case 9: Test the swapcase_string function with a string that contains non-English characters.
    """
    assert swapcase_string("héllo wörld") == "HÉLLO WÖRLD", (
        "Failed on string with non-English characters"
    )


def test_swapcase_string_mixed_whitespace() -> None:
    """
    Test case 10: Test the swapcase_string function with a string that contains mixed whitespace characters.
    """
    assert swapcase_string(" \t\nHello World\t\n ") == " \t\nhELLO wORLD\t\n ", (
        "Failed on string with mixed whitespace characters"
    )


def test_swapcase_string_invalid_type() -> None:
    """
    Test case 11: Test the swapcase_string function with an invalid type.
    """
    with pytest.raises(TypeError):
        swapcase_string(12345)
