import pytest
from typing import Any
from iterable_functions.flatten_list import flatten_list


def test_flatten_list_success() -> None:
    """
    Test case 1: Test the flatten_list function with valid inputs.
    """
    list_to_flatten: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    expected_output: list[int] = [1, 2, 3, 4, 5, 6]
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_empty_list() -> None:
    """
    Test case 2: Test the flatten_list function with an empty list.
    """
    list_to_flatten: list[list[int]] = []
    expected_output: list[int] = []
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_empty_sublists() -> None:
    """
    Test case 3: Test the flatten_list function with empty sublists.
    """
    list_to_flatten: list[list[int]] = [[], [], []]
    expected_output: list[int] = []
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_strings() -> None:
    """
    Test case 4: Test the flatten_list function with lists of strings.
    """
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
    Test case 5: Test the flatten_list function with lists of mixed types.
    """
    list_to_flatten: list[list[Any]] = [
        [1, "banana"], [3.14, "apple"], [True, None]]
    expected_output: list[Any] = [1, "banana", 3.14, "apple", True, None]
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_nested_levels() -> None:
    """
    Test case 6: Test the flatten_list function with several levels of nested lists.
    """
    list_to_flatten: list[list[Any]] = [[1, [2, 3]], [4, [5, 6]], [7, [8, 9]]]
    expected_output: list[Any] = [1, [2, 3], 4, [5, 6], 7, [8, 9]]
    assert flatten_list(list_to_flatten) == expected_output


def test_flatten_list_type_error_list() -> None:
    """
    Test case 7: Test the flatten_list function with invalid type for list_to_flatten.
    """
    with pytest.raises(TypeError):
        flatten_list("not a list of lists")


def test_flatten_list_type_error_elements() -> None:
    """
    Test case 8: Test the flatten_list function with invalid elements in list_to_flatten.
    """
    with pytest.raises(TypeError):
        flatten_list([[1, 2], "not a list"])
