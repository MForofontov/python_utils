import pytest
from iterable_functions.set_operations.set_cartesian_product_as_list import (
    set_cartesian_product_as_list,
)


def test_set_cartesian_product_as_list_two_sets() -> None:
    """
    Test case 1: Cartesian product of two sets as list.
    """
    set1 = {1, 2}
    set2 = {"a", "b"}
    result = set_cartesian_product_as_list(set1, set2)
    assert len(result) == 4
    # Check that it's a list, not a set
    assert isinstance(result, list)
    # Check that all combinations are present
    assert (1, "a") in result
    assert (2, "b") in result


def test_set_cartesian_product_as_list_three_sets() -> None:
    """
    Test case 2: Cartesian product of three sets as list.
    """
    set1 = {1, 2}
    set2 = {"a", "b"}
    set3 = {"x", "y"}
    result = set_cartesian_product_as_list(set1, set2, set3)
    assert len(result) == 8  # 2 * 2 * 2 = 8
    assert isinstance(result, list)
    # Check that result is sorted
    assert result == sorted(result)


def test_set_cartesian_product_as_list_single_set() -> None:
    """
    Test case 3: Cartesian product of single set as list.
    """
    set1 = {1, 2, 3}
    expected = [(1,), (2,), (3,)]
    result = set_cartesian_product_as_list(set1)
    assert result == expected


def test_set_cartesian_product_as_list_empty_set() -> None:
    """
    Test case 4: Cartesian product including empty set.
    """
    set1 = {1, 2}
    set2 = set()
    expected = []
    result = set_cartesian_product_as_list(set1, set2)
    assert result == expected


def test_set_cartesian_product_as_list_strings() -> None:
    """
    Test case 5: Cartesian product with string elements.
    """
    set1 = {"a", "b"}
    set2 = {"1", "2"}
    result = set_cartesian_product_as_list(set1, set2)
    assert len(result) == 4
    assert isinstance(result, list)
    # Check that result is sorted
    assert result == sorted(result)


def test_set_cartesian_product_as_list_mixed_types() -> None:
    """
    Test case 6: Cartesian product with mixed types.
    """
    set1 = {1, 2}
    set2 = {"a", "b"}
    set3 = {3.14, 2.71}
    result = set_cartesian_product_as_list(set1, set2, set3)
    assert len(result) == 8  # 2 * 2 * 2 = 8
    assert isinstance(result, list)
    # Check that result is sorted
    assert result == sorted(result)


def test_set_cartesian_product_as_list_large_sets() -> None:
    """
    Test case 7: Test with larger sets.
    """
    set1 = {1, 2, 3}
    set2 = {"a", "b", "c"}
    set3 = {"x", "y"}
    result = set_cartesian_product_as_list(set1, set2, set3)
    assert len(result) == 18  # 3 * 3 * 2 = 18
    assert isinstance(result, list)
    # Check that result is sorted
    assert result == sorted(result)
def test_set_cartesian_product_as_list_no_sets() -> None:
    """
    Test case 8: ValueError when no sets provided.
    """
    with pytest.raises(ValueError, match="At least one set must be provided"):
        set_cartesian_product_as_list()


def test_set_cartesian_product_as_list_type_error() -> None:
    """
    Test case 9: TypeError for non-set arguments.
    """
    with pytest.raises(TypeError, match="All arguments must be sets"):
        set_cartesian_product_as_list({1, 2}, "not a set")


def test_set_cartesian_product_as_list_type_error_position() -> None:
    """
    Test case 10: TypeError with position information.
    """
    with pytest.raises(TypeError, match="got list at position 1"):
        set_cartesian_product_as_list({1, 2}, [3, 4])
