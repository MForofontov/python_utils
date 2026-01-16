import pytest
from iterable_functions.set_operations.set_symmetric_difference import (
    get_unique_elements_across_sets,
    set_symmetric_difference,
)


def test_set_symmetric_difference_two_sets() -> None:
    """
    Test case 1: Symmetric difference of two sets.
    """
    set1 = {1, 2, 3}
    set2 = {2, 3, 4}
    result = set_symmetric_difference(set1, set2)
    expected = {1, 4}
    assert result == expected


def test_set_symmetric_difference_three_sets() -> None:
    """
    Test case 2: Symmetric difference of three sets.
    """
    set1 = {1, 2, 3}
    set2 = {2, 3, 4}
    set3 = {3, 4, 5}
    result = set_symmetric_difference(set1, set2, set3)
    expected = {1, 3, 5}
    assert result == expected


def test_set_symmetric_difference_identical_sets() -> None:
    """
    Test case 3: Symmetric difference of identical sets.
    """
    set1 = {1, 2, 3}
    set2 = {1, 2, 3}
    set3 = {1, 2, 3}
    result = set_symmetric_difference(set1, set2, set3)
    expected = {1, 2, 3}
    assert result == expected


def test_set_symmetric_difference_empty_sets() -> None:
    """
    Test case 4: Symmetric difference including empty sets.
    """
    set1 = {1, 2, 3}
    set2 = set()
    result = set_symmetric_difference(set1, set2)
    assert result == {1, 2, 3}


def test_set_symmetric_difference_strings() -> None:
    """
    Test case 5: Symmetric difference with string elements.
    """
    set1 = {"a", "b", "c"}
    set2 = {"b", "c", "d"}
    result = set_symmetric_difference(set1, set2)
    expected = {"a", "d"}
    assert result == expected


def test_set_symmetric_difference_mixed_types() -> None:
    """
    Test case 6: Symmetric difference with mixed types.
    """
    set1 = {1, "a", 3.14}
    set2 = {1, "b", 2.71}
    result = set_symmetric_difference(set1, set2)
    expected = {"a", 3.14, "b", 2.71}
    assert result == expected


def test_set_symmetric_difference_four_sets() -> None:
    """
    Test case 7: Symmetric difference of four sets.
    """
    set1 = {1, 2, 3, 4}
    set2 = {2, 3, 4, 5}
    set3 = {3, 4, 5, 6}
    set4 = {4, 5, 6, 7}
    result = set_symmetric_difference(set1, set2, set3, set4)
    # Elements that appear in an odd number of sets: 1, 3, 5, 7
    expected = {1, 3, 5, 7}
    assert result == expected


def test_set_symmetric_difference_single_element() -> None:
    """
    Test case 8: Symmetric difference with single elements.
    """
    set1 = {1}
    set2 = {2}
    result = set_symmetric_difference(set1, set2)
    expected = {1, 2}
    assert result == expected


def test_get_unique_elements_across_sets_basic() -> None:
    """
    Test case 9: Basic test for get_unique_elements_across_sets with two sets.
    """
    result = get_unique_elements_across_sets({1, 2, 3}, {2, 3, 4})
    assert isinstance(result, list)
    assert sorted(result) == [1, 4]


def test_get_unique_elements_across_sets_three_sets() -> None:
    """
    Test case 10: Test get_unique_elements_across_sets with three sets.
    """
    result = get_unique_elements_across_sets({1, 2}, {2, 3}, {3, 4})
    assert isinstance(result, list)
    assert sorted(result) == [1, 4]


def test_set_symmetric_difference_type_error() -> None:
    """
    Test case 11: TypeError for non-set arguments.
    """
    with pytest.raises(TypeError, match="All arguments must be sets"):
        set_symmetric_difference({1, 2}, "not a set")


def test_set_symmetric_difference_value_error() -> None:
    """
    Test case 12: ValueError for fewer than 2 sets.
    """
    with pytest.raises(ValueError, match="At least 2 sets must be provided"):
        set_symmetric_difference({1, 2})


def test_get_unique_elements_across_sets_value_error() -> None:
    """
    Test case 13: ValueError when fewer than 2 sets provided.
    """
    with pytest.raises(ValueError, match="At least 2 sets must be provided"):
        get_unique_elements_across_sets({1, 2})


def test_get_unique_elements_across_sets_type_error() -> None:
    """
    Test case 14: TypeError when non-set argument provided.
    """
    with pytest.raises(TypeError, match="All arguments must be sets"):
        get_unique_elements_across_sets({1, 2}, [3, 4])
