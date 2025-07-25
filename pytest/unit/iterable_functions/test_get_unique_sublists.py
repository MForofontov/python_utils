import pytest
from typing import Any
from iterable_functions.get_unique_sublists import get_unique_sublists


def test_get_unique_sublists_success() -> None:
    """
    Test the get_unique_sublists function with valid inputs.
    """
    # Test case 1: Valid inputs
    list_of_lists: list[list[int]] = [[1, 2], [3, 4], [1, 2], [5, 6]]
    expected_output: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_no_duplicates() -> None:
    """
    Test the get_unique_sublists function with no duplicates.
    """
    # Test case 2: No duplicates
    list_of_lists: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    expected_output: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_empty_list() -> None:
    """
    Test the get_unique_sublists function with an empty list of lists.
    """
    # Test case 3: Empty list of lists
    list_of_lists: list[list[int]] = []
    expected_output: list[list[int]] = []
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_empty_sublists() -> None:
    """
    Test the get_unique_sublists function with empty sublists.
    """
    # Test case 4: Empty sublists
    list_of_lists: list[list[int]] = [[], [], []]
    expected_output: list[list[int]] = [[]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_strings() -> None:
    """
    Test the get_unique_sublists function with lists of strings.
    """
    # Test case 5: Lists of strings
    list_of_lists: list[list[str]] = [
        ["apple", "banana"],
        ["cherry", "date"],
        ["apple", "banana"],
    ]
    expected_output: list[list[str]] = [["apple", "banana"], ["cherry", "date"]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_mixed_types() -> None:
    """
    Test the get_unique_sublists function with lists of mixed types.
    """
    # Test case 6: Lists of mixed types
    list_of_lists: list[list[Any]] = [[1, "banana"], [3.14, "apple"], [1, "banana"]]
    expected_output: list[list[Any]] = [[1, "banana"], [3.14, "apple"]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_type_error_list_of_lists() -> None:
    """
    Test the get_unique_sublists function with invalid type for list_of_lists.
    """
    # Test case 7: Invalid type for list_of_lists
    with pytest.raises(TypeError):
        get_unique_sublists("not a list of lists")


def test_get_unique_sublists_type_error_elements() -> None:
    """
    Test the get_unique_sublists function with invalid elements in list_of_lists.
    """
    # Test case 8: Invalid elements in list_of_lists
    with pytest.raises(TypeError):
        get_unique_sublists([[1, 2], "not a list"])


def test_get_unique_sublists_unhashable_elements() -> None:
    """
    Test the get_unique_sublists function with unhashable elements in sublists.
    """
    # Test case 9: Unhashable elements in sublists
    with pytest.raises(TypeError):
        get_unique_sublists([[1, 2], [{3: 4}, 5]])
