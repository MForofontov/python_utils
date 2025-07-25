import pytest
from typing import Any
from iterable_functions.any_match_lists import any_match_lists


def test_any_match_lists_integers() -> None:
    """
    Test the any_match_lists function with lists of integers.
    """
    # Test case 1: Lists of integers
    list1: list[int] = [1, 2, 6]
    list2: list[int] = [1, 2, 3, 4, 5]
    assert any_match_lists(list1, list2) == True


def test_any_match_lists_strings() -> None:
    """
    Test the any_match_lists function with lists of strings.
    """
    # Test case 2: Lists of strings
    list1: list[str] = ["apple", "banana"]
    list2: list[str] = ["apple", "orange", "grape"]
    assert any_match_lists(list1, list2) == True


def test_any_match_lists_mixed_types() -> None:
    """
    Test the any_match_lists function with lists of mixed types.
    """
    # Test case 3: Lists of mixed types
    list1: list[Any] = [1, "banana", 3.14]
    list2: list[Any] = ["apple", 1, "grape"]
    assert any_match_lists(list1, list2) == True


def test_any_match_lists_floats() -> None:
    """
    Test the any_match_lists function with lists of floats.
    """
    # Test case 4: Lists of floats
    list1: list[float] = [1.1, 2.2, 6.6]
    list2: list[float] = [1.1, 2.2, 3.3, 4.4, 5.5]
    assert any_match_lists(list1, list2) == True


def test_any_match_lists_booleans() -> None:
    """
    Test the any_match_lists function with lists of booleans.
    """
    # Test case 5: Lists of booleans
    list1: list[bool] = [True, False]
    list2: list[bool] = [True, True, False]
    assert any_match_lists(list1, list2) == True


def test_any_match_lists_empty_lists() -> None:
    """
    Test the any_match_lists function with two empty lists.
    """
    # Test case 6: Two empty lists
    list1: list[int] = []
    list2: list[int] = []
    assert any_match_lists(list1, list2) == False


def test_any_match_lists_no_match() -> None:
    """
    Test the any_match_lists function with valid inputs where no elements match.
    """
    # Test case 7: No elements match
    list1: list[int] = [6, 7, 8]
    list2: list[int] = [1, 2, 3, 4, 5]
    assert any_match_lists(list1, list2) == False


def test_any_match_lists_empty_list1() -> None:
    """
    Test the any_match_lists function with an empty list1.
    """
    # Test case 8: Empty list1
    list1: list[int] = []
    list2: list[int] = [1, 2, 3, 4, 5]
    assert any_match_lists(list1, list2) == False


def test_any_match_lists_empty_list2() -> None:
    """
    Test the any_match_lists function with an empty list2.
    """
    # Test case 9: Empty list2
    list1: list[int] = [1, 2, 3]
    list2: list[int] = []
    assert any_match_lists(list1, list2) == False


def test_any_match_lists_unhashable_elements() -> None:
    """
    Test the any_match_lists function with unhashable elements.
    """
    # Test case 10: Unhashable elements
    list1: list[Any] = [[1, 2], [3, 4]]
    list2: list[Any] = [[1, 2], [5, 6]]
    assert any_match_lists(list1, list2) == True


def test_any_match_lists_type_error_list1() -> None:
    """
    Test the any_match_lists function with invalid type for list1.
    """
    # Test case 11: Invalid type for list1
    with pytest.raises(TypeError):
        any_match_lists("not a list", [1, 2, 3])


def test_any_match_lists_type_error_list2() -> None:
    """
    Test the any_match_lists function with invalid type for list2.
    """
    # Test case 12: Invalid type for list2
    with pytest.raises(TypeError):
        any_match_lists([1, 2, 3], "not a list")
