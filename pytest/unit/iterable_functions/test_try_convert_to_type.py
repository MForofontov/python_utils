import pytest
from typing import Any
from iterable_functions.try_convert_to_type import try_convert_to_type

def test_try_convert_to_type_success_int() -> None:
    """
    Test the try_convert_to_type function with valid integer conversion.
    """
    value = "123"
    target_type = int
    expected_output = 123
    assert try_convert_to_type(value, target_type) == expected_output

def test_try_convert_to_type_success_float() -> None:
    """
    Test the try_convert_to_type function with valid float conversion.
    """
    value = "123.45"
    target_type = float
    expected_output = 123.45
    assert try_convert_to_type(value, target_type) == expected_output

def test_try_convert_to_type_success_str() -> None:
    """
    Test the try_convert_to_type function with valid string conversion.
    """
    value = 123
    target_type = str
    expected_output = "123"
    assert try_convert_to_type(value, target_type) == expected_output

def test_try_convert_to_type_invalid_conversion() -> None:
    """
    Test the try_convert_to_type function with an invalid conversion.
    """
    value = "abc"
    target_type = int
    with pytest.raises(ValueError):
        try_convert_to_type(value, target_type)

def test_try_convert_to_type_type_error() -> None:
    """
    Test the try_convert_to_type function with invalid type for target_type.
    """
    with pytest.raises(TypeError):
        try_convert_to_type("123", "not a type")

def test_try_convert_to_type_success_list() -> None:
    """
    Test the try_convert_to_type function with list conversion.
    """
    value = (1, 2, 3)
    target_type = list
    expected_output = [1, 2, 3]
    assert try_convert_to_type(value, target_type) == expected_output

def test_try_convert_to_type_success_bool() -> None:
    """
    Test the try_convert_to_type function with bool conversion.
    """
    value = 0
    target_type = bool
    expected_output = False
    assert try_convert_to_type(value, target_type) is expected_output

def test_try_convert_to_type_custom_class() -> None:
    """
    Test the try_convert_to_type function with a custom class.
    """
    class Custom:
        def __init__(self, val: Any) -> None:
            self.val = int(val)

        def __eq__(self, other: object) -> bool:  # pragma: no cover - simple equality
            return isinstance(other, Custom) and self.val == other.val

    value = "5"
    target_type = Custom
    expected_output = Custom(5)
    assert try_convert_to_type(value, target_type) == expected_output

def test_try_convert_to_type_invalid_list_conversion() -> None:
    """
    Test the try_convert_to_type function when conversion to list fails.
    """
    value = 1
    target_type = list
    with pytest.raises(ValueError):
        try_convert_to_type(value, target_type)
