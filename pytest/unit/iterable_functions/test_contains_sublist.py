import pytest
from typing import Any
from iterable_functions.contains_sublist import contains_sublist

def test_contains_sublist_success() -> None:
    """
    Test the contains_sublist function with valid inputs where the main list is fully contained in a sublist.
    """
    # Test case 1: Main list is fully contained in a sublist
    main_list: list[int] = [1, 2]
    list_of_lists: list[list[int]] = [[1, 2, 3], [4, 5, 6]]
    assert contains_sublist(main_list, list_of_lists) == True

def test_contains_sublist_no_match() -> None:
    """
    Test the contains_sublist function with valid inputs where the main list is not fully contained in any sublist.
    """
    # Test case 2: Main list is not fully contained in any sublist
    main_list: list[int] = [1, 2, 7]
    list_of_lists: list[list[int]] = [[1, 2, 3], [4, 5, 6]]
    assert contains_sublist(main_list, list_of_lists) == False

def test_contains_sublist_empty_main_list() -> None:
    """
    Test the contains_sublist function with an empty main list.
    """
    # Test case 3: Empty main list
    main_list: list[int] = []
    list_of_lists: list[list[int]] = [[1, 2, 3], [4, 5, 6]]
    assert contains_sublist(main_list, list_of_lists) == True

def test_contains_sublist_empty_list_of_lists() -> None:
    """
    Test the contains_sublist function with an empty list of lists.
    """
    # Test case 4: Empty list of lists
    main_list: list[int] = [1, 2]
    list_of_lists: list[list[int]] = []
    assert contains_sublist(main_list, list_of_lists) == False

def test_contains_sublist_two_empty_lists() -> None:
    """
    Test the contains_sublist function with two empty lists.
    """
    # Test case 5: Two empty lists
    main_list: list[int] = []
    list_of_lists: list[list[int]] = []
    assert contains_sublist(main_list, list_of_lists) == False

def test_contains_sublist_list_with_empty_lists() -> None:
    """
    Test the contains_sublist function with a list containing empty lists.
    """
    # Test case 6: List with empty lists
    main_list: list[int] = [1, 2]
    list_of_lists: list[list[int]] = [[], [], []]
    assert contains_sublist(main_list, list_of_lists) == False

def test_contains_sublist_strings() -> None:
    """
    Test the contains_sublist function with lists of strings.
    """
    # Test case 7: Lists of strings
    main_list: list[str] = ["apple", "banana"]
    list_of_lists: list[list[str]] = [["apple", "banana", "cherry"], ["date", "fig", "grape"]]
    assert contains_sublist(main_list, list_of_lists) == True

def test_contains_sublist_mixed_types() -> None:
    """
    Test the contains_sublist function with lists of mixed types.
    """
    # Test case 8: Lists of mixed types
    main_list: list[Any] = [1, "banana", 3.14]
    list_of_lists: list[list[Any]] = [[1, "banana", 3.14], ["apple", 1, "grape"]]
    assert contains_sublist(main_list, list_of_lists) == True

def test_contains_sublist_type_error_main_list() -> None:
    """
    Test the contains_sublist function with invalid type for main_list.
    """
    # Test case 9: Invalid type for main_list
    with pytest.raises(TypeError):
        contains_sublist("not a list", [[1, 2, 3]])

def test_contains_sublist_type_error_list_of_lists() -> None:
    """
    Test the contains_sublist function with invalid type for list_of_lists.
    """
    # Test case 10: Invalid type for list_of_lists
    with pytest.raises(TypeError):
        contains_sublist([1, 2], "not a list of lists")

def test_contains_sublist_type_error_list_of_lists_elements() -> None:
    """
    Test the contains_sublist function with invalid elements in list_of_lists.
    """
    # Test case 11: Invalid elements in list_of_lists
    with pytest.raises(TypeError):
        contains_sublist([1, 2], [[1, 2, 3], "not a list"])
