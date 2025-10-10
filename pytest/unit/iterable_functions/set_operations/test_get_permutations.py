import pytest
from iterable_functions.set_operations.get_permutations import get_permutations


def test_get_permutations_normal_case() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    input_set = {1, 2, 3}
    r = 2
    expected = [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]
    result = get_permutations(input_set, r)
    assert result == expected


def test_get_permutations_r_none() -> None:
    """
    Test case 2: Test with r=None (all elements).
    """
    input_set = {1, 2, 3}
    expected = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    result = get_permutations(input_set)
    assert result == expected


def test_get_permutations_r_equals_0() -> None:
    """
    Test case 3: Test with r=0 (empty permutations).
    """
    input_set = {1, 2, 3}
    r = 0
    expected = [[]]
    result = get_permutations(input_set, r)
    assert result == expected


def test_get_permutations_single_element() -> None:
    """
    Test case 4: Test with single element set.
    """
    input_set = {1}
    r = 1
    expected = [[1]]
    result = get_permutations(input_set, r)
    assert result == expected


def test_get_permutations_strings() -> None:
    """
    Test case 5: Test with string elements.
    """
    input_set = {"a", "b"}
    r = 2
    expected = [["a", "b"], ["b", "a"]]
    result = get_permutations(input_set, r)
    assert result == expected


def test_get_permutations_boundary_r_equals_1() -> None:
    """
    Test case 6: Boundary test with r=1.
    """
    input_set = {1, 2, 3}
    r = 1
    expected = [[1], [2], [3]]
    result = get_permutations(input_set, r)
    assert result == expected


def test_get_permutations_large_set() -> None:
    """
    Test case 7: Test with larger set.
    """
    input_set = {1, 2, 3, 4}
    r = 2
    result = get_permutations(input_set, r)
    # Should return 12 permutations for P(4,2)
    assert len(result) == 12
    # Each permutation should have exactly 2 elements
    assert all(len(perm) == 2 for perm in result)
def test_get_permutations_empty_set() -> None:
    """
    Test case 8: Test with empty set.
    """
    input_set = set()
    r = 2
    with pytest.raises(ValueError, match="r cannot be larger than set size"):
        get_permutations(input_set, r)


def test_get_permutations_type_error_input_set() -> None:
    """
    Test case 9: TypeError for invalid input_set type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        get_permutations("not a set", 2)


def test_get_permutations_type_error_r() -> None:
    """
    Test case 10: TypeError for invalid r type.
    """
    input_set = {1, 2, 3}
    with pytest.raises(TypeError, match="r must be an int or None"):
        get_permutations(input_set, "not an int")


def test_get_permutations_value_error_negative_r() -> None:
    """
    Test case 11: ValueError for negative r.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="r must be non-negative"):
        get_permutations(input_set, -1)


def test_get_permutations_value_error_r_too_large() -> None:
    """
    Test case 12: ValueError for r larger than set size.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="r cannot be larger than set size 3"):
        get_permutations(input_set, 4)
