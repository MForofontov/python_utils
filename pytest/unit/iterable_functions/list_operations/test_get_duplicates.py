from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from python_utils.iterable_functions.list_operations.get_duplicates import get_duplicates


def test_get_duplicates_success() -> None:
    """
    Test case 1: Test the get_duplicates function with valid inputs.
    """
    input_list: list[int] = [1, 2, 2, 3, 4, 4, 5]
    expected_output: list[int] = [2, 4]
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_no_duplicates() -> None:
    """
    Test case 2: Test the get_duplicates function with no duplicates.
    """
    input_list: list[int] = [1, 2, 3, 4, 5]
    expected_output: list[int] = []
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_empty_list() -> None:
    """
    Test case 3: Test the get_duplicates function with an empty list.
    """
    input_list: list[int] = []
    expected_output: list[int] = []
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_strings() -> None:
    """
    Test case 4: Test the get_duplicates function with a list of strings.
    """
    input_list: list[str] = ["apple", "banana", "apple", "cherry", "banana"]
    expected_output: list[str] = ["apple", "banana"]
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_mixed_types() -> None:
    """
    Test case 5: Test the get_duplicates function with a list of mixed types.
    """
    input_list: list[Any] = [1, "banana", 1, "apple", 3.14, "banana"]
    expected_output: list[Any] = [1, "banana"]
    assert get_duplicates(input_list) == expected_output


def test_get_duplicates_unhashable_elements() -> None:
    """
    Test case 6: Test the get_duplicates function with unhashable elements.
    """
    input_list: list[Any] = [[1, 2], [1, 2], [3, 4]]
    with pytest.raises(TypeError):
        get_duplicates(input_list)


def test_get_duplicates_type_error() -> None:
    """
    Test case 7: Test the get_duplicates function with invalid type for input_list.
    """
    with pytest.raises(TypeError):
        get_duplicates("not a list")
