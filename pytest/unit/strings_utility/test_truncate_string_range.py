import pytest
from strings_utility.truncate_string_range import truncate_string_range


def test_truncate_string_range_basic() -> None:
    """
    Test the truncate_string_range function with a basic string and valid range.
    """
    # Test case 1: Basic string and valid range
    assert (
        truncate_string_range("hello world", 0, 5) == "hello"
    ), "Failed on basic string and valid range"


def test_truncate_string_range_middle() -> None:
    """
    Test the truncate_string_range function with a string and a range in the middle.
    """
    # Test case 2: String and a range in the middle
    assert (
        truncate_string_range("python programming", 7, 18) == "programming"
    ), "Failed on string and a range in the middle"


def test_truncate_string_range_end() -> None:
    """
    Test the truncate_string_range function with a string and a range at the end.
    """
    # Test case 3: String and a range at the end
    assert (
        truncate_string_range("1234567890", 2, 5) == "345"
    ), "Failed on string and a range at the end"


def test_truncate_string_range_full() -> None:
    """
    Test the truncate_string_range function with a string and a range covering the full string.
    """
    # Test case 4: String and a range covering the full string
    assert (
        truncate_string_range("truncate", 0, 8) == "truncate"
    ), "Failed on string and a range covering the full string"


def test_truncate_string_range_empty_string() -> None:
    """
    Test the truncate_string_range function with an empty string.
    """
    # Test case 5: Empty string
    assert truncate_string_range("", 0, 0) == "", "Failed on empty string"


def test_truncate_string_range_negative_indices() -> None:
    """
    Test the truncate_string_range function with negative indices.
    """
    # Test case 6: Negative indices
    assert (
        truncate_string_range("hello world", -5, -1) == "worl"
    ), "Failed on negative indices"


def test_truncate_string_range_invalid_start() -> None:
    """
    Test the truncate_string_range function with an invalid start index.
    """
    # Test case 7: Invalid start index
    with pytest.raises(ValueError):
        truncate_string_range("hello world", 5, 0)


def test_truncate_string_range_invalid_string_type() -> None:
    """
    Test the truncate_string_range function with an invalid string type.
    """
    # Test case 8: Invalid string type
    with pytest.raises(TypeError):
        truncate_string_range(12345, 0, 5)


def test_truncate_string_range_invalid_start_type() -> None:
    """
    Test the truncate_string_range function with an invalid start index type.
    """
    # Test case 9: Invalid start index type
    with pytest.raises(TypeError):
        truncate_string_range("hello world", "0", 5)


def test_truncate_string_range_invalid_end_type() -> None:
    """
    Test the truncate_string_range function with an invalid end index type.
    """
    # Test case 10: Invalid end index type
    with pytest.raises(TypeError):
        truncate_string_range("hello world", 0, "5")
