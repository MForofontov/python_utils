import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from pyutils_collection.iterable_functions.set_operations.set_cartesian_product import (
    set_cartesian_product,
)


def test_set_cartesian_product_two_sets() -> None:
    """
    Test case 1: Cartesian product of two sets.
    """
    set1 = {1, 2}
    set2 = {"a", "b"}
    expected = {(1, "a"), (1, "b"), (2, "a"), (2, "b")}
    result = set_cartesian_product(set1, set2)
    assert result == expected


def test_set_cartesian_product_three_sets() -> None:
    """
    Test case 2: Cartesian product of three sets.
    """
    set1 = {1, 2}
    set2 = {"a", "b"}
    set3 = {"x", "y"}
    result = set_cartesian_product(set1, set2, set3)
    assert len(result) == 8  # 2 * 2 * 2 = 8
    # Check that all combinations are present
    assert (1, "a", "x") in result
    assert (2, "b", "y") in result


def test_set_cartesian_product_single_set() -> None:
    """
    Test case 3: Cartesian product of single set.
    """
    set1 = {1, 2, 3}
    expected = {(1,), (2,), (3,)}
    result = set_cartesian_product(set1)
    assert result == expected


def test_set_cartesian_product_empty_set() -> None:
    """
    Test case 4: Cartesian product including empty set.
    """
    set1 = {1, 2}
    set2 = set()
    expected = set()
    result = set_cartesian_product(set1, set2)
    assert result == expected


def test_set_cartesian_product_strings() -> None:
    """
    Test case 5: Cartesian product with string elements.
    """
    set1 = {"a", "b"}
    set2 = {"1", "2"}
    expected = {("a", "1"), ("a", "2"), ("b", "1"), ("b", "2")}
    result = set_cartesian_product(set1, set2)
    assert result == expected


def test_set_cartesian_product_mixed_types() -> None:
    """
    Test case 6: Cartesian product with mixed types.
    """
    set1 = {1, 2}
    set2 = {"a", "b"}
    set3 = {3.14, 2.71}
    result = set_cartesian_product(set1, set2, set3)
    assert len(result) == 8  # 2 * 2 * 2 = 8
    # Check types are preserved
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 3


def test_set_cartesian_product_large_sets() -> None:
    """
    Test case 7: Test with larger sets.
    """
    set1 = {1, 2, 3}
    set2 = {"a", "b", "c"}
    set3 = {"x", "y"}
    result = set_cartesian_product(set1, set2, set3)
    assert len(result) == 18  # 3 * 3 * 2 = 18


def test_set_cartesian_product_no_sets() -> None:
    """
    Test case 8: ValueError when no sets provided.
    """
    with pytest.raises(ValueError, match="At least one set must be provided"):
        set_cartesian_product()


def test_set_cartesian_product_type_error() -> None:
    """
    Test case 9: TypeError for non-set arguments.
    """
    with pytest.raises(TypeError, match="All arguments must be sets"):
        set_cartesian_product({1, 2}, "not a set")


def test_set_cartesian_product_type_error_position() -> None:
    """
    Test case 10: TypeError with position information.
    """
    with pytest.raises(TypeError, match="got list at position 1"):
        set_cartesian_product({1, 2}, [3, 4])
