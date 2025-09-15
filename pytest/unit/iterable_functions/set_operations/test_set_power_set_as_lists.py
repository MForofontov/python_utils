import pytest
from iterable_functions.set_operations.set_power_set_as_lists import (
    set_power_set_as_lists,
)


def test_set_power_set_as_lists_normal_case() -> None:
    """
    Test case 1: Power set as lists for a normal set.
    """
    input_set = {1, 2, 3}
    result = set_power_set_as_lists(input_set)
    # Power set should have 8 elements (2^3)
    assert len(result) == 8
    # Check that empty list is first
    assert result[0] == []
    # Check that full set is last
    assert result[-1] == [1, 2, 3]
    # Check some subsets
    assert [] in result
    assert [1] in result
    assert [1, 2] in result
    assert [2, 3] in result


def test_set_power_set_as_lists_empty_set() -> None:
    """
    Test case 2: Power set as lists of empty set.
    """
    input_set = set()
    result = set_power_set_as_lists(input_set)
    expected = [[]]
    assert result == expected


def test_set_power_set_as_lists_single_element() -> None:
    """
    Test case 3: Power set as lists of single element set.
    """
    input_set = {1}
    result = set_power_set_as_lists(input_set)
    expected = [[], [1]]
    assert result == expected


def test_set_power_set_as_lists_two_elements() -> None:
    """
    Test case 4: Power set as lists of two element set.
    """
    input_set = {1, 2}
    result = set_power_set_as_lists(input_set)
    expected = [[], [1], [2], [1, 2]]
    assert result == expected


def test_set_power_set_as_lists_strings() -> None:
    """
    Test case 5: Power set as lists with string elements.
    """
    input_set = {"a", "b"}
    result = set_power_set_as_lists(input_set)
    expected = [[], ["a"], ["b"], ["a", "b"]]
    assert result == expected


def test_set_power_set_as_lists_mixed_types() -> None:
    """
    Test case 6: Power set as lists with mixed types.
    """
    input_set = {1, "a"}
    result = set_power_set_as_lists(input_set)
    expected = [[], [1], ["a"], [1, "a"]]
    assert result == expected


def test_set_power_set_as_lists_type_error() -> None:
    """
    Test case 7: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        set_power_set_as_lists("not a set")


def test_set_power_set_as_lists_large_set() -> None:
    """
    Test case 8: Test with larger set.
    """
    input_set = {1, 2, 3, 4}
    result = set_power_set_as_lists(input_set)
    # Power set should have 16 elements (2^4)
    assert len(result) == 16
    # Check that result is sorted by length then lexicographically
    assert result[0] == []  # Empty set first
    assert result[1:5] == [[1], [2], [3], [4]]  # Single elements
    assert result[-1] == [1, 2, 3, 4]  # Full set last


def test_set_power_set_as_lists_ordering() -> None:
    """
    Test case 9: Test that ordering is correct.
    """
    input_set = {3, 1, 2}
    result = set_power_set_as_lists(input_set)
    # Should be sorted by length, then lexicographically
    expected = [
        [],  # length 0
        [1],
        [2],
        [3],  # length 1, sorted
        [1, 2],
        [1, 3],
        [2, 3],  # length 2, sorted
        [1, 2, 3],  # length 3
    ]
    assert result == expected
