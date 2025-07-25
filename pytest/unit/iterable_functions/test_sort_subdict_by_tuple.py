import pytest
from collections import OrderedDict
from iterable_functions.sort_subdict_by_tuple import sort_subdict_by_tuple


def test_sort_subdict_by_tuple_success() -> None:
    """
    Test the sort_subdict_by_tuple function with valid inputs.
    """
    dict_ = {"a": {"x": 1, "y": 2, "z": 3}, "b": {"y": 4, "x": 5, "z": 6}}
    order = ("x", "y", "z")
    expected_output = {
        "a": OrderedDict([("x", 1), ("y", 2), ("z", 3)]),
        "b": OrderedDict([("x", 5), ("y", 4), ("z", 6)]),
    }
    assert sort_subdict_by_tuple(dict_, order) == expected_output


def test_sort_subdict_by_tuple_partial_order() -> None:
    """
    Test the sort_subdict_by_tuple function with a partial order.
    """
    dict_ = {"a": {"x": 1, "y": 2, "z": 3}, "b": {"y": 4, "x": 5, "z": 6}}
    order = ("y", "x")
    expected_output = {
        "a": OrderedDict([("y", 2), ("x", 1), ("z", 3)]),
        "b": OrderedDict([("y", 4), ("x", 5), ("z", 6)]),
    }
    assert sort_subdict_by_tuple(dict_, order) == expected_output


def test_sort_subdict_by_tuple_empty_order() -> None:
    """
    Test the sort_subdict_by_tuple function with an empty order.
    """
    dict_ = {"a": {"x": 1, "y": 2, "z": 3}, "b": {"y": 4, "x": 5, "z": 6}}
    order = ()
    expected_output = {
        "a": OrderedDict([("x", 1), ("y", 2), ("z", 3)]),
        "b": OrderedDict([("y", 4), ("x", 5), ("z", 6)]),
    }
    assert sort_subdict_by_tuple(dict_, order) == expected_output


def test_sort_subdict_by_tuple_type_error_dict() -> None:
    """
    Test the sort_subdict_by_tuple function with invalid type for dict_.
    """
    with pytest.raises(TypeError):
        sort_subdict_by_tuple("not a dict", ("x", "y", "z"))


def test_sort_subdict_by_tuple_type_error_order() -> None:
    """
    Test the sort_subdict_by_tuple function with invalid type for order.
    """
    with pytest.raises(TypeError):
        sort_subdict_by_tuple({"a": {"x": 1, "y": 2}}, "not a tuple")


def test_sort_subdict_by_tuple_type_error_order_elements() -> None:
    """
    Test the sort_subdict_by_tuple function with invalid elements in order.
    """
    with pytest.raises(TypeError):
        sort_subdict_by_tuple({"a": {"x": 1, "y": 2}}, (1, 2, 3))
