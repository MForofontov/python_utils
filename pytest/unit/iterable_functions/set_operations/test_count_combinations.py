import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from python_utils.iterable_functions.set_operations.count_combinations import count_combinations


def test_count_combinations_normal_case() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    input_set = {1, 2, 3, 4, 5}
    r = 2
    expected = 10  # C(5,2) = 10
    result = count_combinations(input_set, r)
    assert result == expected


def test_count_combinations_r_equals_3() -> None:
    """
    Test case 2: Test with r=3.
    """
    input_set = {1, 2, 3, 4, 5}
    r = 3
    expected = 10  # C(5,3) = 10
    result = count_combinations(input_set, r)
    assert result == expected


def test_count_combinations_r_equals_0() -> None:
    """
    Test case 3: Test with r=0.
    """
    input_set = {1, 2, 3}
    r = 0
    expected = 1  # C(n,0) = 1
    result = count_combinations(input_set, r)
    assert result == expected


def test_count_combinations_r_equals_n() -> None:
    """
    Test case 4: Test with r equal to set size.
    """
    input_set = {1, 2, 3}
    r = 3
    expected = 1  # C(3,3) = 1
    result = count_combinations(input_set, r)
    assert result == expected


def test_count_combinations_empty_set() -> None:
    """
    Test case 5: Test with empty set.
    """
    input_set = set()
    r = 0
    expected = 1  # C(0,0) = 1
    result = count_combinations(input_set, r)
    assert result == expected


def test_count_combinations_single_element() -> None:
    """
    Test case 6: Test with single element set.
    """
    input_set = {1}
    r = 1
    expected = 1  # C(1,1) = 1
    result = count_combinations(input_set, r)
    assert result == expected


def test_count_combinations_large_set() -> None:
    """
    Test case 7: Test with larger set.
    """
    input_set = set(range(10))  # 10 elements
    r = 3
    expected = 120  # C(10,3) = 120
    result = count_combinations(input_set, r)
    assert result == expected


def test_count_combinations_boundary_values() -> None:
    """
    Test case 8: Test boundary values.
    """
    # Test C(4,1) = 4
    assert count_combinations({1, 2, 3, 4}, 1) == 4
    # Test C(4,4) = 1
    assert count_combinations({1, 2, 3, 4}, 4) == 1
    # Test C(4,0) = 1
    assert count_combinations({1, 2, 3, 4}, 0) == 1


def test_count_combinations_type_error_input_set() -> None:
    """
    Test case 9: TypeError for invalid input_set type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        count_combinations("not a set", 2)


def test_count_combinations_type_error_r() -> None:
    """
    Test case 10: TypeError for invalid r type.
    """
    input_set = {1, 2, 3}
    with pytest.raises(TypeError, match="r must be an int"):
        count_combinations(input_set, "not an int")


def test_count_combinations_value_error_negative_r() -> None:
    """
    Test case 11: ValueError for negative r.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="r must be non-negative"):
        count_combinations(input_set, -1)


def test_count_combinations_value_error_r_too_large() -> None:
    """
    Test case 12: ValueError for r larger than set size.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="r cannot be larger than set size 3"):
        count_combinations(input_set, 4)
