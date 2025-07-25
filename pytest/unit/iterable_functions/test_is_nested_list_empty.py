import pytest
from typing import Any
from iterable_functions.is_nested_list_empty import is_nested_list_empty


def test_is_list_empty_success() -> None:
    """
    Test the is_list_empty function with valid inputs.
    """
    # Test case 1: Valid inputs
    input_list: list[Any] = []
    expected_output: bool = True
    assert is_nested_list_empty(input_list) == expected_output


def test_is_list_empty_nested_empty_lists() -> None:
    """
    Test the is_list_empty function with nested empty lists.
    """
    # Test case 2: Nested empty lists
    input_list: list[Any] = [[], [[]], [[], [[]]]]
    expected_output: bool = True
    assert is_nested_list_empty(input_list) == expected_output


def test_is_list_empty_non_empty_list() -> None:
    """
    Test the is_list_empty function with a non-empty list.
    """
    # Test case 3: Non-empty list
    input_list: list[Any] = [1, 2, 3]
    expected_output: bool = False
    assert is_nested_list_empty(input_list) == expected_output


def test_is_list_empty_mixed_nested_lists() -> None:
    """
    Test the is_list_empty function with mixed nested lists.
    """
    # Test case 4: Mixed nested lists
    input_list: list[Any] = [[], [1, 2], [[], [3]]]
    expected_output: bool = False
    assert is_nested_list_empty(input_list) == expected_output


def test_is_list_empty_type_error() -> None:
    """
    Test the is_list_empty function with invalid type for input_list.
    """
    # Test case 5: Invalid type for input_list
    with pytest.raises(TypeError):
        is_nested_list_empty("not a list")
