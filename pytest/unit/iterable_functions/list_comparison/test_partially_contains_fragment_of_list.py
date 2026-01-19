from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from iterable_functions.list_comparison.partially_contains_fragment_of_list import (
    partially_contains_fragment_of_list,
)


def test_partially_contains_fragment_of_list_success() -> None:
    """
    Test case 1: Test the partially_contains_fragment_of_list function with valid inputs.
    """
    target_list: list[str] = ["a", "b"]
    list_of_lists: list[list[str]] = [["a", "b", "c"], ["d", "e"]]
    expected_output: bool = True
    assert (
        partially_contains_fragment_of_list(target_list, list_of_lists)
        == expected_output
    )


def test_partially_contains_fragment_of_list_not_found() -> None:
    """
    Test case 2: Test the partially_contains_fragment_of_list function with target_list not found.
    """
    target_list: list[str] = ["a", "b"]
    list_of_lists: list[list[str]] = [["d", "e"], ["f", "g"]]
    expected_output: bool = False
    assert (
        partially_contains_fragment_of_list(target_list, list_of_lists)
        == expected_output
    )


def test_partially_contains_fragment_of_list_empty_target_list() -> None:
    """
    Test case 3: Test the partially_contains_fragment_of_list function with an empty target_list.
    """
    target_list: list[str] = []
    list_of_lists: list[list[str]] = [["a", "b", "c"], ["d", "e"]]
    expected_output: bool = True
    assert (
        partially_contains_fragment_of_list(target_list, list_of_lists)
        == expected_output
    )


def test_partially_contains_fragment_of_list_empty_list_of_lists() -> None:
    """
    Test case 4: Test the partially_contains_fragment_of_list function with an empty list_of_lists.
    """
    target_list: list[str] = ["a", "b"]
    list_of_lists: list[list[str]] = []
    expected_output: bool = False
    assert (
        partially_contains_fragment_of_list(target_list, list_of_lists)
        == expected_output
    )


def test_partially_contains_fragment_of_list_integers() -> None:
    """
    Test case 5: Test the partially_contains_fragment_of_list function with lists of integers.
    """
    target_list: list[int] = [1, 2]
    list_of_lists: list[list[int]] = [[1, 2, 3], [4, 5, 6]]
    expected_output: bool = True
    assert (
        partially_contains_fragment_of_list(target_list, list_of_lists)
        == expected_output
    )


def test_partially_contains_fragment_of_list_mixed_types() -> None:
    """
    Test case 6: Test the partially_contains_fragment_of_list function with mixed types.
    """
    target_list: list[Any] = [1, "b"]
    list_of_lists: list[list[Any]] = [[1, "b", 3], ["d", "e"]]
    expected_output: bool = True
    assert (
        partially_contains_fragment_of_list(target_list, list_of_lists)
        == expected_output
    )


def test_partially_contains_fragment_of_list_type_error_target_list() -> None:
    """
    Test case 7: Test the partially_contains_fragment_of_list function with invalid type for target_list.
    """
    with pytest.raises(TypeError):
        partially_contains_fragment_of_list("not a list", [["a", "b", "c"], ["d", "e"]])


def test_partially_contains_fragment_of_list_type_error_list_of_lists() -> None:
    """
    Test case 8: Test the partially_contains_fragment_of_list function with invalid type for list_of_lists.
    """
    with pytest.raises(TypeError):
        partially_contains_fragment_of_list(["a", "b"], "not a list of lists")


def test_partially_contains_fragment_of_list_type_error_elements() -> None:
    """
    Test case 9: Test the partially_contains_fragment_of_list function with invalid elements in list_of_lists.
    """
    with pytest.raises(TypeError):
        partially_contains_fragment_of_list(["a", "b"], [["a", "b", "c"], "not a list"])
