import pytest
from typing import Any
from iterable_functions.is_nested_list_empty import is_nested_list_empty


def test_is_list_empty_success() -> None:
    """
    Test case 1: Test the is_list_empty function with valid inputs.
    """
    input_list: list[Any] = []
    expected_output: bool = True
    assert is_nested_list_empty(input_list) == expected_output


def test_is_list_empty_nested_empty_lists() -> None:
    """
    Test case 2: Test the is_list_empty function with nested empty lists.
    """
    input_list: list[Any] = [[], [[]], [[], [[]]]]
    expected_output: bool = True
    assert is_nested_list_empty(input_list) == expected_output


def test_is_list_empty_non_empty_list() -> None:
    """
    Test case 3: Test the is_list_empty function with a non-empty list.
    """
    input_list: list[Any] = [1, 2, 3]
    expected_output: bool = False
    assert is_nested_list_empty(input_list) == expected_output


def test_is_list_empty_mixed_nested_lists() -> None:
    """
    Test case 4: Test the is_list_empty function with mixed nested lists.
    """
    input_list: list[Any] = [[], [1, 2], [[], [3]]]
    expected_output: bool = False
    assert is_nested_list_empty(input_list) == expected_output


def test_is_list_empty_type_error() -> None:
    """
    Test case 5: Test the is_list_empty function with invalid type for input_list.
    """
    with pytest.raises(TypeError):
        is_nested_list_empty("not a list")
