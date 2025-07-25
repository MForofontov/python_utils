import pytest
from typing import Any
from iterable_functions.check_if_all_sets_are_same import check_if_all_sets_are_same


def test_check_if_all_sets_are_same_identical_sets() -> None:
    """
    Test the check_if_all_sets_are_same function with identical sets.
    """
    # Test case 1: Identical sets
    sets_list: list[set[int]] = [{1, 2, 3}, {1, 2, 3}, {1, 2, 3}]
    assert check_if_all_sets_are_same(sets_list) == True


def test_check_if_all_sets_are_same_different_sets() -> None:
    """
    Test the check_if_all_sets_are_same function with different sets.
    """
    # Test case 2: Different sets
    sets_list: list[set[int]] = [{1, 2, 3}, {4, 5, 6}, {1, 2, 3}]
    assert check_if_all_sets_are_same(sets_list) == False


def test_check_if_all_sets_are_same_single_set() -> None:
    """
    Test the check_if_all_sets_are_same function with a single set.
    """
    # Test case 3: Single set
    sets_list: list[set[int]] = [{1, 2, 3}]
    assert check_if_all_sets_are_same(sets_list) == True


def test_check_if_all_sets_are_same_empty_list() -> None:
    """
    Test the check_if_all_sets_are_same function with an empty list.
    """
    # Test case 4: Empty list
    sets_list: list[set[int]] = []
    assert check_if_all_sets_are_same(sets_list) == True


def test_check_if_all_sets_are_same_empty_sets() -> None:
    """
    Test the check_if_all_sets_are_same function with empty sets.
    """
    # Test case 5: Empty sets
    sets_list: list[set[int]] = [set(), set(), set()]
    assert check_if_all_sets_are_same(sets_list) == True


def test_check_if_all_sets_are_same_strings() -> None:
    """
    Test the check_if_all_sets_are_same function with sets of strings.
    """
    # Test case 6: Sets of strings
    sets_list: list[set[str]] = [
        {"apple", "banana"},
        {"apple", "banana"},
        {"apple", "banana"},
    ]
    assert check_if_all_sets_are_same(sets_list) == True


def test_check_if_all_sets_are_same_mixed_types() -> None:
    """
    Test the check_if_all_sets_are_same function with sets of mixed types.
    """
    # Test case 7: Sets of mixed types
    sets_list: list[set[Any]] = [
        {1, "banana", 3.14},
        {1, "banana", 3.14},
        {1, "banana", 3.14},
    ]
    assert check_if_all_sets_are_same(sets_list) == True


def test_check_if_all_sets_are_same_type_error() -> None:
    """
    Test the check_if_all_sets_are_same function with invalid type for sets_list.
    """
    # Test case 8: Invalid type for sets_list
    with pytest.raises(TypeError):
        check_if_all_sets_are_same("not a list")


def test_check_if_all_sets_are_same_type_error_elements() -> None:
    """
    Test the check_if_all_sets_are_same function with invalid elements in sets_list.
    """
    # Test case 9: Invalid elements in sets_list
    with pytest.raises(TypeError):
        check_if_all_sets_are_same([{1, 2, 3}, "not a set"])
