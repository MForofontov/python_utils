import pytest
from strings_utility.truncate_string_range import truncate_string_range


def test_truncate_string_range_basic() -> None:
    """
    Test case 1: Test the truncate_string_range function with a basic string and valid range.
    """
    assert truncate_string_range("hello world", 0, 5) == "hello", (
        "Failed on basic string and valid range"
    )


def test_truncate_string_range_middle() -> None:
    """
    Test case 2: Test the truncate_string_range function with a string and a range in the middle.
    """
    assert truncate_string_range("python programming", 7, 18) == "programming", (
        "Failed on string and a range in the middle"
    )


def test_truncate_string_range_end() -> None:
    """
    Test case 3: Test the truncate_string_range function with a string and a range at the end.
    """
    assert truncate_string_range("1234567890", 2, 5) == "345", (
        "Failed on string and a range at the end"
    )


def test_truncate_string_range_full() -> None:
    """
    Test case 4: Test the truncate_string_range function with a string and a range covering the full string.
    """
    assert truncate_string_range("truncate", 0, 8) == "truncate", (
        "Failed on string and a range covering the full string"
    )


def test_truncate_string_range_empty_string() -> None:
    """
    Test case 5: Test the truncate_string_range function with an empty string.
    """
    assert truncate_string_range("", 0, 0) == "", "Failed on empty string"


def test_truncate_string_range_negative_indices() -> None:
    """
    Test case 6: Test the truncate_string_range function with negative indices.
    """
    assert truncate_string_range("hello world", -5, -1) == "worl", (
        "Failed on negative indices"
    )


def test_truncate_string_range_invalid_start() -> None:
    """
    Test case 7: Test the truncate_string_range function with an invalid start index.
    """
    with pytest.raises(ValueError):
        truncate_string_range("hello world", 5, 0)


def test_truncate_string_range_invalid_string_type() -> None:
    """
    Test case 8: Test the truncate_string_range function with an invalid string type.
    """
    with pytest.raises(TypeError):
        truncate_string_range(12345, 0, 5)


def test_truncate_string_range_invalid_start_type() -> None:
    """
    Test case 9: Test the truncate_string_range function with an invalid start index type.
    """
    with pytest.raises(TypeError):
        truncate_string_range("hello world", "0", 5)


def test_truncate_string_range_invalid_end_type() -> None:
    """
    Test case 10: Test the truncate_string_range function with an invalid end index type.
    """
    with pytest.raises(TypeError):
        truncate_string_range("hello world", 0, "5")
