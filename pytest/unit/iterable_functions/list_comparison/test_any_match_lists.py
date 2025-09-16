from typing import Any

import pytest
from iterable_functions.list_comparison.any_match_lists import any_match_lists


def test_any_match_lists_integers() -> None:
    """
    Test case 1: Test the any_match_lists function with lists of integers.
    """
    list1: list[int] = [1, 2, 6]
    list2: list[int] = [1, 2, 3, 4, 5]
    assert any_match_lists(list1, list2)


def test_any_match_lists_strings() -> None:
    """
    Test case 2: Test the any_match_lists function with lists of strings.
    """
    list1: list[str] = ["apple", "banana"]
    list2: list[str] = ["apple", "orange", "grape"]
    assert any_match_lists(list1, list2)


def test_any_match_lists_mixed_types() -> None:
    """
    Test case 3: Test the any_match_lists function with lists of mixed types.
    """
    list1: list[Any] = [1, "banana", 3.14]
    list2: list[Any] = ["apple", 1, "grape"]
    assert any_match_lists(list1, list2)


def test_any_match_lists_floats() -> None:
    """
    Test case 4: Test the any_match_lists function with lists of floats.
    """
    list1: list[float] = [1.1, 2.2, 6.6]
    list2: list[float] = [1.1, 2.2, 3.3, 4.4, 5.5]
    assert any_match_lists(list1, list2)


def test_any_match_lists_booleans() -> None:
    """
    Test case 5: Test the any_match_lists function with lists of booleans.
    """
    list1: list[bool] = [True, False]
    list2: list[bool] = [True, True, False]
    assert any_match_lists(list1, list2)


def test_any_match_lists_empty_lists() -> None:
    """
    Test case 6: Test the any_match_lists function with two empty lists.
    """
    list1: list[int] = []
    list2: list[int] = []
    assert not any_match_lists(list1, list2)


def test_any_match_lists_no_match() -> None:
    """
    Test case 7: Test the any_match_lists function with valid inputs where no elements match.
    """
    list1: list[int] = [6, 7, 8]
    list2: list[int] = [1, 2, 3, 4, 5]
    assert not any_match_lists(list1, list2)


def test_any_match_lists_empty_list1() -> None:
    """
    Test case 8: Test the any_match_lists function with an empty list1.
    """
    list1: list[int] = []
    list2: list[int] = [1, 2, 3, 4, 5]
    assert not any_match_lists(list1, list2)


def test_any_match_lists_empty_list2() -> None:
    """
    Test case 9: Test the any_match_lists function with an empty list2.
    """
    list1: list[int] = [1, 2, 3]
    list2: list[int] = []
    assert not any_match_lists(list1, list2)


def test_any_match_lists_unhashable_elements() -> None:
    """
    Test case 10: Test the any_match_lists function with unhashable elements.
    """
    list1: list[Any] = [[1, 2], [3, 4]]
    list2: list[Any] = [[1, 2], [5, 6]]
    assert any_match_lists(list1, list2)


def test_any_match_lists_type_error_list1() -> None:
    """
    Test case 11: Test the any_match_lists function with invalid type for list1.
    """
    with pytest.raises(TypeError):
        any_match_lists("not a list", [1, 2, 3])


def test_any_match_lists_type_error_list2() -> None:
    """
    Test case 12: Test the any_match_lists function with invalid type for list2.
    """
    with pytest.raises(TypeError):
        any_match_lists([1, 2, 3], "not a list")
