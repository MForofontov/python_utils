import pytest
from typing import Any
from iterable_functions.list_comparison.find_sublist_index import find_sublist_index


def test_find_sublist_index_success() -> None:
    """
    Test case 1: Test the find_sublist_index function with valid inputs where the target value is found.
    """
    input_list_of_lists: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    target_value: int = 4
    expected_output: int = 1
    assert find_sublist_index(input_list_of_lists, target_value) == expected_output


def test_find_sublist_index_not_found() -> None:
    """
    Test case 2: Test the find_sublist_index function with valid inputs where the target value is not found.
    """
    input_list_of_lists: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    target_value: int = 7
    expected_output: None = None
    assert find_sublist_index(input_list_of_lists, target_value) == expected_output


def test_find_sublist_index_empty_list() -> None:
    """
    Test case 3: Test the find_sublist_index function with an empty list of lists.
    """
    input_list_of_lists: list[list[int]] = []
    target_value: int = 1
    expected_output: None = None
    assert find_sublist_index(input_list_of_lists, target_value) == expected_output


def test_find_sublist_index_empty_sublists() -> None:
    """
    Test case 4: Test the find_sublist_index function with empty sublists.
    """
    input_list_of_lists: list[list[int]] = [[], [], []]
    target_value: int = 1
    expected_output: None = None
    assert find_sublist_index(input_list_of_lists, target_value) == expected_output


def test_find_sublist_index_strings() -> None:
    """
    Test case 5: Test the find_sublist_index function with lists of strings.
    """
    input_list_of_lists: list[list[str]] = [
        ["apple", "banana"],
        ["cherry", "date"],
        ["fig", "grape"],
    ]
    target_value: str = "date"
    expected_output: int = 1
    assert find_sublist_index(input_list_of_lists, target_value) == expected_output


def test_find_sublist_index_mixed_types() -> None:
    """
    Test case 6: Test the find_sublist_index function with lists of mixed types.
    """
    input_list_of_lists: list[list[Any]] = [
        [1, "banana"],
        [3.14, "apple"],
        [True, None],
    ]
    target_value: Any = "apple"
    expected_output: int = 1
    assert find_sublist_index(input_list_of_lists, target_value) == expected_output


def test_find_sublist_index_type_error_input_list_of_lists() -> None:
    """
    Test case 7: Test the find_sublist_index function with invalid type for input_list_of_lists.
    """
    with pytest.raises(TypeError):
        find_sublist_index("not a list of lists", 1)


def test_find_sublist_index_type_error_elements() -> None:
    """
    Test case 8: Test the find_sublist_index function with invalid elements in input_list_of_lists.
    """
    with pytest.raises(TypeError):
        find_sublist_index([[1, 2], "not a list"], 1)
