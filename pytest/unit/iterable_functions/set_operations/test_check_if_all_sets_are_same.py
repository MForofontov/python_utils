from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from python_utils.iterable_functions.set_operations.check_if_all_sets_are_same import (
    check_if_all_sets_are_same,
)


def test_check_if_all_sets_are_same_identical_sets() -> None:
    """
    Test case 1: Test the check_if_all_sets_are_same function with identical sets.
    """
    sets_list: list[set[int]] = [{1, 2, 3}, {1, 2, 3}, {1, 2, 3}]
    assert check_if_all_sets_are_same(sets_list)


def test_check_if_all_sets_are_same_different_sets() -> None:
    """
    Test case 2: Test the check_if_all_sets_are_same function with different sets.
    """
    sets_list: list[set[int]] = [{1, 2, 3}, {4, 5, 6}, {1, 2, 3}]
    assert not check_if_all_sets_are_same(sets_list)


def test_check_if_all_sets_are_same_single_set() -> None:
    """
    Test case 3: Test the check_if_all_sets_are_same function with a single set.
    """
    sets_list: list[set[int]] = [{1, 2, 3}]
    assert check_if_all_sets_are_same(sets_list)


def test_check_if_all_sets_are_same_empty_list() -> None:
    """
    Test case 4: Test the check_if_all_sets_are_same function with an empty list.
    """
    sets_list: list[set[int]] = []
    assert check_if_all_sets_are_same(sets_list)


def test_check_if_all_sets_are_same_empty_sets() -> None:
    """
    Test case 5: Test the check_if_all_sets_are_same function with empty sets.
    """
    sets_list: list[set[int]] = [set(), set(), set()]
    assert check_if_all_sets_are_same(sets_list)


def test_check_if_all_sets_are_same_strings() -> None:
    """
    Test case 6: Test the check_if_all_sets_are_same function with sets of strings.
    """
    sets_list: list[set[str]] = [
        {"apple", "banana"},
        {"apple", "banana"},
        {"apple", "banana"},
    ]
    assert check_if_all_sets_are_same(sets_list)


def test_check_if_all_sets_are_same_mixed_types() -> None:
    """
    Test case 7: Test the check_if_all_sets_are_same function with sets of mixed types.
    """
    sets_list: list[set[Any]] = [
        {1, "banana", 3.14},
        {1, "banana", 3.14},
        {1, "banana", 3.14},
    ]
    assert check_if_all_sets_are_same(sets_list)


def test_check_if_all_sets_are_same_type_error() -> None:
    """
    Test case 8: Test the check_if_all_sets_are_same function with invalid type for sets_list.
    """
    with pytest.raises(TypeError):
        check_if_all_sets_are_same("not a list")


def test_check_if_all_sets_are_same_type_error_elements() -> None:
    """
    Test case 9: Test the check_if_all_sets_are_same function with invalid elements in sets_list.
    """
    with pytest.raises(TypeError):
        check_if_all_sets_are_same([{1, 2, 3}, "not a set"])
