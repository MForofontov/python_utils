from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from pyutils_collection.iterable_functions.set_operations.convert_set_elements_to_strings import (
    convert_set_elements_to_strings,
)


def test_convert_set_elements_to_strings_success() -> None:
    """
    Test case 1: Test the convert_set_elements_to_strings function with valid inputs.
    """
    input_set: set[Any] = {1, 2, 3, "a", "b", "c"}
    expected_output: set[str] = {"1", "2", "3", "a", "b", "c"}
    assert convert_set_elements_to_strings(input_set) == expected_output


def test_convert_set_elements_to_strings_empty_set() -> None:
    """
    Test case 2: Test the convert_set_elements_to_strings function with an empty set.
    """
    input_set: set[Any] = set()
    expected_output: set[str] = set()
    assert convert_set_elements_to_strings(input_set) == expected_output


def test_convert_set_elements_to_strings_mixed_types() -> None:
    """
    Test case 3: Test the convert_set_elements_to_strings function with mixed types.
    """
    input_set: set[Any] = {2, "a", 3.14, True}
    expected_output: set[str] = {"2", "a", "3.14", "True"}
    assert convert_set_elements_to_strings(input_set) == expected_output


def test_convert_set_elements_to_strings_nested_elements() -> None:
    """
    Test case 4: Test the convert_set_elements_to_strings function with nested elements.
    """
    input_set: set[Any] = {1, "a", (1, 2)}
    expected_output: set[str] = {"1", "a", "(1, 2)"}
    assert convert_set_elements_to_strings(input_set) == expected_output


def test_convert_set_elements_to_strings_type_error() -> None:
    """
    Test case 5: Test the convert_set_elements_to_strings function with invalid type for input_set.
    """
    with pytest.raises(TypeError):
        convert_set_elements_to_strings("not a set")
