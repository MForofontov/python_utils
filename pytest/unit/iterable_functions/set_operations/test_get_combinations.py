import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from iterable_functions.set_operations.get_combinations import get_combinations


def test_get_combinations_normal_case() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    input_set = {1, 2, 3, 4}
    r = 2
    expected = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    result = get_combinations(input_set, r)
    assert result == expected


def test_get_combinations_r_equals_3() -> None:
    """
    Test case 2: Test with r=3.
    """
    input_set = {1, 2, 3, 4}
    r = 3
    expected = [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
    result = get_combinations(input_set, r)
    assert result == expected


def test_get_combinations_r_equals_0() -> None:
    """
    Test case 3: Test with r=0 (empty combinations).
    """
    input_set = {1, 2, 3}
    r = 0
    expected = [[]]
    result = get_combinations(input_set, r)
    assert result == expected


def test_get_combinations_r_equals_n() -> None:
    """
    Test case 4: Test with r equal to set size.
    """
    input_set = {1, 2, 3}
    r = 3
    expected = [[1, 2, 3]]
    result = get_combinations(input_set, r)
    assert result == expected


def test_get_combinations_single_element() -> None:
    """
    Test case 5: Test with single element set.
    """
    input_set = {1}
    r = 1
    expected = [[1]]
    result = get_combinations(input_set, r)
    assert result == expected


def test_get_combinations_strings() -> None:
    """
    Test case 6: Test with string elements.
    """
    input_set = {"a", "b", "c"}
    r = 2
    expected = [["a", "b"], ["a", "c"], ["b", "c"]]
    result = get_combinations(input_set, r)
    assert result == expected


def test_get_combinations_boundary_r_equals_1() -> None:
    """
    Test case 7: Boundary test with r=1.
    """
    input_set = {1, 2, 3}
    r = 1
    expected = [[1], [2], [3]]
    result = get_combinations(input_set, r)
    assert result == expected


def test_get_combinations_large_set() -> None:
    """
    Test case 8: Performance test with larger set.
    """
    input_set = set(range(10))
    r = 3
    result = get_combinations(input_set, r)
    # Should return 120 combinations for C(10,3)
    assert len(result) == 120
    # Each combination should have exactly 3 elements
    assert all(len(comb) == 3 for comb in result)


def test_get_combinations_empty_set() -> None:
    """
    Test case 9: Test with empty set.
    """
    input_set = set()
    r = 2
    with pytest.raises(ValueError, match="r cannot be larger than set size 0"):
        get_combinations(input_set, r)


def test_get_combinations_type_error_input_set() -> None:
    """
    Test case 10: TypeError for invalid input_set type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        get_combinations("not a set", 2)


def test_get_combinations_type_error_r() -> None:
    """
    Test case 11: TypeError for invalid r type.
    """
    input_set = {1, 2, 3}
    with pytest.raises(TypeError, match="r must be an int"):
        get_combinations(input_set, "not an int")


def test_get_combinations_value_error_negative_r() -> None:
    """
    Test case 12: ValueError for negative r.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="r must be non-negative"):
        get_combinations(input_set, -1)


def test_get_combinations_value_error_r_too_large() -> None:
    """
    Test case 13: ValueError for r larger than set size.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="r cannot be larger than set size 3"):
        get_combinations(input_set, 4)
