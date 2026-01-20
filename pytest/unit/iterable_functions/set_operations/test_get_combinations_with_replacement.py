import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from pyutils_collection.iterable_functions.set_operations.get_combinations_with_replacement import (
    get_combinations_with_replacement,
)


def test_get_combinations_with_replacement_normal_case() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    input_set = {1, 2, 3}
    r = 2
    expected = [[1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
    result = get_combinations_with_replacement(input_set, r)
    assert result == expected


def test_get_combinations_with_replacement_r_equals_3() -> None:
    """
    Test case 2: Test with r=3.
    """
    input_set = {1, 2}
    r = 3
    expected = [[1, 1, 1], [1, 1, 2], [1, 2, 2], [2, 2, 2]]
    result = get_combinations_with_replacement(input_set, r)
    assert result == expected


def test_get_combinations_with_replacement_r_equals_0() -> None:
    """
    Test case 3: Test with r=0 (empty combinations).
    """
    input_set = {1, 2, 3}
    r = 0
    expected = [[]]
    result = get_combinations_with_replacement(input_set, r)
    assert result == expected


def test_get_combinations_with_replacement_empty_set() -> None:
    """
    Test case 4: Test with empty set.
    """
    input_set = set()
    r = 2
    expected = []
    result = get_combinations_with_replacement(input_set, r)
    assert result == expected


def test_get_combinations_with_replacement_single_element() -> None:
    """
    Test case 5: Test with single element set.
    """
    input_set = {1}
    r = 3
    expected = [[1, 1, 1]]
    result = get_combinations_with_replacement(input_set, r)
    assert result == expected


def test_get_combinations_with_replacement_strings() -> None:
    """
    Test case 6: Test with string elements.
    """
    input_set = {"a", "b"}
    r = 2
    expected = [["a", "a"], ["a", "b"], ["b", "b"]]
    result = get_combinations_with_replacement(input_set, r)
    assert result == expected


def test_get_combinations_with_replacement_boundary_r_equals_1() -> None:
    """
    Test case 7: Boundary test with r=1.
    """
    input_set = {1, 2, 3}
    r = 1
    expected = [[1], [2], [3]]
    result = get_combinations_with_replacement(input_set, r)
    assert result == expected


def test_get_combinations_with_replacement_large_set() -> None:
    """
    Test case 8: Test with larger set.
    """
    input_set = {1, 2, 3, 4}
    r = 2
    result = get_combinations_with_replacement(input_set, r)
    # Should return 10 combinations for C(4,2) with replacement
    assert len(result) == 10
    # Each combination should have exactly 2 elements
    assert all(len(comb) == 2 for comb in result)


def test_get_combinations_with_replacement_type_error_input_set() -> None:
    """
    Test case 9: TypeError for invalid input_set type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        get_combinations_with_replacement("not a set", 2)


def test_get_combinations_with_replacement_type_error_r() -> None:
    """
    Test case 10: TypeError for invalid r type.
    """
    input_set = {1, 2, 3}
    with pytest.raises(TypeError, match="r must be an int"):
        get_combinations_with_replacement(input_set, "not an int")


def test_get_combinations_with_replacement_value_error_negative_r() -> None:
    """
    Test case 11: ValueError for negative r.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="r must be non-negative"):
        get_combinations_with_replacement(input_set, -1)
