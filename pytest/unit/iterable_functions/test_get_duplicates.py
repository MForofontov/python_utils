import pytest
from typing import Any
from iterable_functions.get_duplicates import get_duplicates


def test_get_duplicates_success() -> None:
    """
    Test the get_duplicates function with valid inputs.
    """
    # Test case 1: Valid inputs
    input_list: list[int] = [1, 2, 2, 3, 4, 4, 5]
    expected_output: list[int] = [2, 4]
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_no_duplicates() -> None:
    """
    Test the get_duplicates function with no duplicates.
    """
    # Test case 2: No duplicates
    input_list: list[int] = [1, 2, 3, 4, 5]
    expected_output: list[int] = []
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_empty_list() -> None:
    """
    Test the get_duplicates function with an empty list.
    """
    # Test case 3: Empty list
    input_list: list[int] = []
    expected_output: list[int] = []
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_strings() -> None:
    """
    Test the get_duplicates function with a list of strings.
    """
    # Test case 4: List of strings
    input_list: list[str] = ["apple", "banana", "apple", "cherry", "banana"]
    expected_output: list[str] = ["apple", "banana"]
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_mixed_types() -> None:
    """
    Test the get_duplicates function with a list of mixed types.
    """
    # Test case 5: List of mixed types
    input_list: list[Any] = [1, "banana", 1, "apple", 3.14, "banana"]
    expected_output: list[Any] = [1, "banana"]
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_unhashable_elements() -> None:
    """
    Test the get_duplicates function with unhashable elements.
    """
    # Test case 6: Unhashable elements
    input_list: list[Any] = [[1, 2], [1, 2], [3, 4]]
    with pytest.raises(TypeError):
        get_duplicates(input_list)


def test_get_duplicates_type_error() -> None:
    """
    Test the get_duplicates function with invalid type for input_list.
    """
    # Test case 7: Invalid type for input_list
    with pytest.raises(TypeError):
        get_duplicates("not a list")
