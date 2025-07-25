import pytest
from typing import Any
from iterable_functions.convert_set_elements_to_strings import (
    convert_set_elements_to_strings,
)


def test_convert_set_elements_to_strings_success() -> None:
    """
    Test the convert_set_elements_to_strings function with valid inputs.
    """
    # Test case 1: Valid inputs
    input_set: set[Any] = {1, 2, 3, "a", "b", "c"}
    expected_output: set[str] = {"1", "2", "3", "a", "b", "c"}
    assert convert_set_elements_to_strings(input_set) == expected_output


def test_convert_set_elements_to_strings_empty_set() -> None:
    """
    Test the convert_set_elements_to_strings function with an empty set.
    """
    # Test case 2: Empty set
    input_set: set[Any] = set()
    expected_output: set[str] = set()
    assert convert_set_elements_to_strings(input_set) == expected_output


def test_convert_set_elements_to_strings_mixed_types() -> None:
    """
    Test the convert_set_elements_to_strings function with mixed types.
    """
    # Test case 3: Mixed types
    input_set: set[Any] = {2, "a", 3.14, True}
    expected_output: set[str] = {"2", "a", "3.14", "True"}
    assert convert_set_elements_to_strings(input_set) == expected_output


def test_convert_set_elements_to_strings_nested_elements() -> None:
    """
    Test the convert_set_elements_to_strings function with nested elements.
    """
    # Test case 4: Nested elements
    input_set: set[Any] = {1, "a", (1, 2)}
    expected_output: set[str] = {"1", "a", "(1, 2)"}
    assert convert_set_elements_to_strings(input_set) == expected_output


def test_convert_set_elements_to_strings_type_error() -> None:
    """
    Test the convert_set_elements_to_strings function with invalid type for input_set.
    """
    # Test case 5: Invalid type for input_set
    with pytest.raises(TypeError):
        convert_set_elements_to_strings("not a set")
