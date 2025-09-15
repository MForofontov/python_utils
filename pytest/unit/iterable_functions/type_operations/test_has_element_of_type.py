import pytest
from typing import Any
from iterable_functions.type_operations.has_element_of_type import has_element_of_type


def test_has_element_of_type_success() -> None:
    """
    Test case 1: Test the has_element_of_type function with valid inputs.
    """
    input_list: list[Any] = [1, "banana", 3.14, True]
    target_type: type = str
    expected_output: bool = True
    assert has_element_of_type(input_list, target_type) == expected_output


def test_has_element_of_type_no_match() -> None:
    """
    Test case 2: Test the has_element_of_type function with no matching elements.
    """
    input_list: list[Any] = [1, 2, 3, 4]
    target_type: type = str
    expected_output: bool = False
    assert has_element_of_type(input_list, target_type) == expected_output


def test_has_element_of_type_empty_list() -> None:
    """
    Test case 3: Test the has_element_of_type function with an empty list.
    """
    input_list: list[Any] = []
    target_type: type = str
    expected_output: bool = False
    assert has_element_of_type(input_list, target_type) == expected_output


def test_has_element_of_type_multiple_matches() -> None:
    """
    Test case 4: Test the has_element_of_type function with multiple matching elements.
    """
    input_list: list[Any] = ["apple", "banana", "cherry"]
    target_type: type = str
    expected_output: bool = True
    assert has_element_of_type(input_list, target_type) == expected_output


def test_has_element_of_type_type_error_list() -> None:
    """
    Test case 5: Test the has_element_of_type function with invalid type for input_list.
    """
    with pytest.raises(TypeError):
        has_element_of_type("not a list", str)


def test_has_element_of_type_type_error_target_type() -> None:
    """
    Test case 6: Test the has_element_of_type function with invalid type for target_type.
    """
    with pytest.raises(TypeError):
        has_element_of_type([1, 2, 3], "not a type")
