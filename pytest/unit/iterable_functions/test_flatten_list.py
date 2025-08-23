import pytest
from typing import Any
from iterable_functions.flatten_list import flatten_list


def test_flatten_list_success() -> None:
    """
    Test the flatten_list function with valid inputs.
    """
    # Test case 1: Valid inputs
    list_to_flatten: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    expected_output: list[int] = [1, 2, 3, 4, 5, 6]
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_empty_list() -> None:
    """
    Test the flatten_list function with an empty list.
    """
    # Test case 2: Empty list
    list_to_flatten: list[list[int]] = []
    expected_output: list[int] = []
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_empty_sublists() -> None:
    """
    Test the flatten_list function with empty sublists.
    """
    # Test case 3: Empty sublists
    list_to_flatten: list[list[int]] = [[], [], []]
    expected_output: list[int] = []
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_strings() -> None:
    """
    Test the flatten_list function with lists of strings.
    """
    # Test case 4: Lists of strings
    list_to_flatten: list[list[str]] = [
        ["apple", "banana"],
        ["cherry", "date"],
        ["fig", "grape"],
    ]
    expected_output: list[str] = [
        "apple", "banana", "cherry", "date", "fig", "grape"]
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_mixed_types() -> None:
    """
    Test the flatten_list function with lists of mixed types.
    """
    # Test case 5: Lists of mixed types
    list_to_flatten: list[list[Any]] = [
        [1, "banana"], [3.14, "apple"], [True, None]]
    expected_output: list[Any] = [1, "banana", 3.14, "apple", True, None]
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_nested_levels() -> None:
    """
    Test the flatten_list function with several levels of nested lists.
    """
    # Test case 6: Several levels of nested lists
    list_to_flatten: list[list[Any]] = [[1, [2, 3]], [4, [5, 6]], [7, [8, 9]]]
    expected_output: list[Any] = [1, [2, 3], 4, [5, 6], 7, [8, 9]]
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_type_error_list() -> None:
    """
    Test the flatten_list function with invalid type for list_to_flatten.
    """
    # Test case 7: Invalid type for list_to_flatten
    with pytest.raises(TypeError):
        flatten_list("not a list of lists")


def test_flatten_list_type_error_elements() -> None:
    """
    Test the flatten_list function with invalid elements in list_to_flatten.
    """
    # Test case 8: Invalid elements in list_to_flatten
    with pytest.raises(TypeError):
        flatten_list([[1, 2], "not a list"])
