from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from iterable_functions.list_operations.check_if_all_elements_are_duplicates import (
    check_if_all_elements_are_duplicates,
)


def test_check_if_all_elements_are_duplicates_all_duplicates() -> None:
    """
    Test case 1: Test the check_if_all_elements_are_duplicates function with all elements being duplicates.
    """
    input_list: list[int] = [1, 1, 2, 2, 3, 3]
    assert check_if_all_elements_are_duplicates(input_list)


def test_check_if_all_elements_are_duplicates_no_duplicates() -> None:
    """
    Test case 2: Test the check_if_all_elements_are_duplicates function with no elements being duplicates.
    """
    input_list: list[int] = [1, 2, 3, 4, 5]
    assert not check_if_all_elements_are_duplicates(input_list)


def test_check_if_all_elements_are_duplicates_some_duplicates() -> None:
    """
    Test case 3: Test the check_if_all_elements_are_duplicates function with some elements being duplicates.
    """
    input_list: list[int] = [1, 1, 2, 3, 4, 4]
    assert not check_if_all_elements_are_duplicates(input_list)


def test_check_if_all_elements_are_duplicates_empty_list() -> None:
    """
    Test case 4: Test the check_if_all_elements_are_duplicates function with an empty list.
    """
    input_list: list[int] = []
    assert not check_if_all_elements_are_duplicates(input_list)


def test_check_if_all_elements_are_duplicates_strings() -> None:
    """
    Test case 5: Test the check_if_all_elements_are_duplicates function with a list of strings.
    """
    input_list: list[str] = ["a", "a", "b", "b", "c", "c"]
    assert check_if_all_elements_are_duplicates(input_list)


def test_check_if_all_elements_are_duplicates_mixed_types() -> None:
    """
    Test case 6: Test the check_if_all_elements_are_duplicates function with a list of mixed types.
    """
    input_list: list[Any] = [1, "a", 1, "a", 3.14, 3.14]
    assert check_if_all_elements_are_duplicates(input_list)


def test_check_if_all_elements_are_duplicates_unhashable_elements() -> None:
    """
    Test case 7: Test the check_if_all_elements_are_duplicates function with unhashable elements.
    """
    input_list: list[Any] = [[1, 2], [1, 2], [3, 4], [3, 4]]
    assert check_if_all_elements_are_duplicates(input_list)


def test_check_if_all_elements_are_duplicates_type_error() -> None:
    """
    Test case 8: Test the check_if_all_elements_are_duplicates function with invalid type for input_list.
    """
    with pytest.raises(TypeError):
        check_if_all_elements_are_duplicates("not a list")
