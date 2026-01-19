from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from python_utils.iterable_functions.list_operations.get_unique_sublists import get_unique_sublists


def test_get_unique_sublists_success() -> None:
    """
    Test case 1: Test the get_unique_sublists function with valid inputs.
    """
    list_of_lists: list[list[int]] = [[1, 2], [3, 4], [1, 2], [5, 6]]
    expected_output: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_no_duplicates() -> None:
    """
    Test case 2: Test the get_unique_sublists function with no duplicates.
    """
    list_of_lists: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    expected_output: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_empty_list() -> None:
    """
    Test case 3: Test the get_unique_sublists function with an empty list of lists.
    """
    list_of_lists: list[list[int]] = []
    expected_output: list[list[int]] = []
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_empty_sublists() -> None:
    """
    Test case 4: Test the get_unique_sublists function with empty sublists.
    """
    list_of_lists: list[list[int]] = [[], [], []]
    expected_output: list[list[int]] = [[]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_strings() -> None:
    """
    Test case 5: Test the get_unique_sublists function with lists of strings.
    """
    list_of_lists: list[list[str]] = [
        ["apple", "banana"],
        ["cherry", "date"],
        ["apple", "banana"],
    ]
    expected_output: list[list[str]] = [["apple", "banana"], ["cherry", "date"]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_mixed_types() -> None:
    """
    Test case 6: Test the get_unique_sublists function with lists of mixed types.
    """
    list_of_lists: list[list[Any]] = [[1, "banana"], [3.14, "apple"], [1, "banana"]]
    expected_output: list[list[Any]] = [[1, "banana"], [3.14, "apple"]]
    assert get_unique_sublists(list_of_lists) == expected_output


def test_get_unique_sublists_type_error_list_of_lists() -> None:
    """
    Test case 7: Test the get_unique_sublists function with invalid type for list_of_lists.
    """
    with pytest.raises(TypeError):
        get_unique_sublists("not a list of lists")


def test_get_unique_sublists_type_error_elements() -> None:
    """
    Test case 8: Test the get_unique_sublists function with invalid elements in list_of_lists.
    """
    with pytest.raises(TypeError):
        get_unique_sublists([[1, 2], "not a list"])


def test_get_unique_sublists_unhashable_elements() -> None:
    """
    Test case 9: Test the get_unique_sublists function with unhashable elements in sublists.
    """
    with pytest.raises(ValueError):
        get_unique_sublists([[1, 2], [{3: 4}, 5]])
