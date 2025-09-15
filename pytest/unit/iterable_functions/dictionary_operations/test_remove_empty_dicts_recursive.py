import pytest
from iterable_functions.remove_empty_dicts_recursive import remove_empty_dicts_recursive


def test_remove_empty_dicts_recursive_success() -> None:
    """
    Test case 1: Test the remove_empty_dicts_recursive function with valid inputs.
    """
    nested_dict = {"a": 1, "b": {}, "c": {"d": {}, "e": 2}, "f": {"g": {"h": {}}}}
    expected_output = {"a": 1, "c": {"e": 2}}
    assert remove_empty_dicts_recursive(nested_dict) == expected_output


def test_remove_empty_dicts_recursive_no_empty_dicts() -> None:
    """
    Test case 2: Test the remove_empty_dicts_recursive function with no empty dictionaries.
    """
    nested_dict = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
    expected_output = nested_dict
    assert remove_empty_dicts_recursive(nested_dict) == expected_output


def test_remove_empty_dicts_recursive_all_empty_dicts() -> None:
    """
    Test case 3: Test the remove_empty_dicts_recursive function with all empty dictionaries.
    """
    nested_dict = {"a": {}, "b": {"c": {}}, "d": {"e": {"f": {}}}}
    expected_output = {}
    assert remove_empty_dicts_recursive(nested_dict) == expected_output


def test_remove_empty_dicts_recursive_mixed_types() -> None:
    test_object = object()
    """
    Test case 4: Test the remove_empty_dicts_recursive function with mixed types.
    """
    nested_dict = {
        "a": 1,
        "b": {"c": {}, "d": 2},
        "e": {"f": {"g": {}, "h": 3}},
        "i": [],
        "j": {"k": test_object, "l": {}, "m": True},
    }
    expected_output = {
        "a": 1,
        "b": {"d": 2},
        "e": {"f": {"h": 3}},
        "i": [],
        "j": {"k": test_object, "m": True},
    }
    assert remove_empty_dicts_recursive(nested_dict) == expected_output


def test_remove_empty_dicts_recursive_type_error() -> None:
    """
    Test case 5: Test the remove_empty_dicts_recursive function with invalid type for nested_dict.
    """
    with pytest.raises(TypeError):
        remove_empty_dicts_recursive("not a dictionary")
