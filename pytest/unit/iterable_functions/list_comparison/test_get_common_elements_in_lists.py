from typing import Any

import pytest
from iterable_functions.list_comparison.get_common_elements_in_lists import (
    get_common_elements_in_lists,
)


def test_get_common_elements_in_lists_success() -> None:
    """
    Test case 1: Test the get_common_elements_in_lists function with valid inputs.
    """
    list_of_lists: list[list[int]] = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    expected_output: list[int] = [3]
    assert get_common_elements_in_lists(list_of_lists) == expected_output


def test_get_common_elements_in_lists_no_common_elements() -> None:
    """
    Test case 2: Test the get_common_elements_in_lists function with no common elements.
    """
    list_of_lists: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    expected_output: list[int] = []
    assert get_common_elements_in_lists(list_of_lists) == expected_output


def test_get_common_elements_in_lists_empty_list() -> None:
    """
    Test case 3: Test the get_common_elements_in_lists function with an empty list of lists.
    """
    list_of_lists: list[list[int]] = []
    expected_output: list[int] = []
    assert get_common_elements_in_lists(list_of_lists) == expected_output


def test_get_common_elements_in_lists_empty_sublists() -> None:
    """
    Test case 4: Test the get_common_elements_in_lists function with empty sublists.
    """
    list_of_lists: list[list[int]] = [[], [], []]
    expected_output: list[int] = []
    assert get_common_elements_in_lists(list_of_lists) == expected_output


def test_get_common_elements_in_lists_strings() -> None:
    """
    Test case 5: Test the get_common_elements_in_lists function with lists of strings.
    """
    list_of_lists: list[list[str]] = [
        ["apple", "banana"],
        ["banana", "cherry"],
        ["banana", "date"],
    ]
    expected_output: list[str] = ["banana"]
    assert get_common_elements_in_lists(list_of_lists) == expected_output


def test_get_common_elements_in_lists_mixed_types() -> None:
    """
    Test case 6: Test the get_common_elements_in_lists function with lists of mixed types.
    """
    list_of_lists: list[list[Any]] = [[1, "banana"], [3.14, "banana"], [True, "banana"]]
    expected_output: list[Any] = ["banana"]
    assert get_common_elements_in_lists(list_of_lists) == expected_output


def test_get_common_elements_in_lists_type_error_list_of_lists() -> None:
    """
    Test case 7: Test the get_common_elements_in_lists function with invalid type for list_of_lists.
    """
    with pytest.raises(TypeError):
        get_common_elements_in_lists("not a list of lists")


def test_get_common_elements_in_lists_type_error_elements() -> None:
    """
    Test case 8: Test the get_common_elements_in_lists function with invalid elements in list_of_lists.
    """
    with pytest.raises(TypeError):
        get_common_elements_in_lists([[1, 2], "not a list"])
