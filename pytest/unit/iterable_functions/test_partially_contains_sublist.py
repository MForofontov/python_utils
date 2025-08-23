import pytest
from typing import Any
from iterable_functions.partially_contains_sublist import partially_contains_sublist


def test_partially_contains_sublist_success() -> None:
    """
    Test the partially_contains_sublist function with valid inputs.
    """
    # Test case 1: Valid inputs
    main_list: list[str] = ["a", "b"]
    list_of_lists: list[list[str]] = [["a", "b", "c"], ["d", "e"]]
    expected_output: bool = True
    assert partially_contains_sublist(
        main_list, list_of_lists) == expected_output


def test_partially_contains_sublist_not_found() -> None:
    """
    Test the partially_contains_sublist function with main_list not found.
    """
    # Test case 2: Main list not found
    main_list: list[str] = ["a", "b"]
    list_of_lists: list[list[str]] = [["d", "e"], ["f", "g"]]
    expected_output: bool = False
    assert partially_contains_sublist(
        main_list, list_of_lists) == expected_output


def test_partially_contains_sublist_empty_main_list() -> None:
    """
    Test the partially_contains_sublist function with an empty main_list.
    """
    # Test case 3: Empty main list
    main_list: list[str] = []
    list_of_lists: list[list[str]] = [["a", "b", "c"], ["d", "e"]]
    expected_output: bool = False
    assert partially_contains_sublist(
        main_list, list_of_lists) == expected_output


def test_partially_contains_sublist_empty_list_of_lists() -> None:
    """
    Test the partially_contains_sublist function with an empty list_of_lists.
    """
    # Test case 4: Empty list of lists
    main_list: list[str] = ["a", "b"]
    list_of_lists: list[list[str]] = []
    expected_output: bool = False
    assert partially_contains_sublist(
        main_list, list_of_lists) == expected_output


def test_partially_contains_sublist_integers() -> None:
    """
    Test the partially_contains_sublist function with lists of integers.
    """
    # Test case 5: Lists of integers
    main_list: list[int] = [1, 2]
    list_of_lists: list[list[int]] = [[1, 2, 3], [4, 5, 6]]
    expected_output: bool = True
    assert partially_contains_sublist(
        main_list, list_of_lists) == expected_output


def test_partially_contains_sublist_mixed_types() -> None:
    """
    Test the partially_contains_sublist function with mixed types.
    """
    # Test case 6: Mixed types
    main_list: list[Any] = [1, "b"]
    list_of_lists: list[list[Any]] = [[1, "b", 3], ["d", "e"]]
    expected_output: bool = True
    assert partially_contains_sublist(
        main_list, list_of_lists) == expected_output


def test_partially_contains_sublist_type_error_main_list() -> None:
    """
    Test the partially_contains_sublist function with invalid type for main_list.
    """
    # Test case 7: Invalid type for main_list
    with pytest.raises(TypeError):
        partially_contains_sublist("not a list", [["a", "b", "c"], ["d", "e"]])


def test_partially_contains_sublist_type_error_list_of_lists() -> None:
    """
    Test the partially_contains_sublist function with invalid type for list_of_lists.
    """
    # Test case 8: Invalid type for list_of_lists
    with pytest.raises(TypeError):
        partially_contains_sublist(["a", "b"], "not a list of lists")


def test_partially_contains_sublist_type_error_elements() -> None:
    """
    Test the partially_contains_sublist function with invalid elements in list_of_lists.
    """
    # Test case 9: Invalid elements in list_of_lists
    with pytest.raises(TypeError):
        partially_contains_sublist(["a", "b"], [["a", "b", "c"], "not a list"])
