import pytest
from typing import Any
from iterable_functions.set_operations.set_power_set import set_power_set


def test_set_power_set_normal_case() -> None:
    """
    Test case 1: Power set of a normal set.
    """
    input_set = {1, 2, 3}
    result = set_power_set(input_set)
    # Power set of {1,2,3} should have 8 elements (2^3)
    assert len(result) == 8
    # Check that empty set is included
    assert frozenset() in result
    # Check that full set is included
    assert frozenset({1, 2, 3}) in result
    # Check some subsets
    assert frozenset({1}) in result
    assert frozenset({1, 2}) in result
    assert frozenset({2, 3}) in result


def test_set_power_set_empty_set() -> None:
    """
    Test case 2: Power set of empty set.
    """
    input_set = set()
    result = set_power_set(input_set)
    expected = {frozenset()}
    assert result == expected


def test_set_power_set_single_element() -> None:
    """
    Test case 3: Power set of single element set.
    """
    input_set = {1}
    result = set_power_set(input_set)
    expected = {frozenset(), frozenset({1})}
    assert result == expected


def test_set_power_set_two_elements() -> None:
    """
    Test case 4: Power set of two element set.
    """
    input_set = {1, 2}
    result = set_power_set(input_set)
    expected = {
        frozenset(),
        frozenset({1}),
        frozenset({2}),
        frozenset({1, 2})
    }
    assert result == expected


def test_set_power_set_strings() -> None:
    """
    Test case 5: Power set with string elements.
    """
    input_set = {"a", "b"}
    result = set_power_set(input_set)
    assert len(result) == 4
    assert frozenset() in result
    assert frozenset({"a", "b"}) in result
    assert frozenset({"a"}) in result
    assert frozenset({"b"}) in result


def test_set_power_set_mixed_types() -> None:
    """
    Test case 6: Power set with mixed types.
    """
    input_set = {1, "a", 3.14}
    result = set_power_set(input_set)
    assert len(result) == 8  # 2^3 = 8
    assert frozenset() in result
    assert frozenset({1, "a", 3.14}) in result


def test_set_power_set_type_error() -> None:
    """
    Test case 7: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        set_power_set("not a set")


def test_set_power_set_large_set() -> None:
    """
    Test case 8: Test with larger set (but not too large to avoid exponential time).
    """
    input_set = {1, 2, 3, 4}
    result = set_power_set(input_set)
    # Power set should have 16 elements (2^4)
    assert len(result) == 16
    # Check that all possible subsets are present
    assert frozenset() in result
    assert frozenset({1, 2, 3, 4}) in result
    assert frozenset({1, 2}) in result
