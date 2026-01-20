import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from pyutils_collection.iterable_functions.set_operations.get_unique_elements_across_sets import (
    get_unique_elements_across_sets,
)
from pyutils_collection.iterable_functions.set_operations.set_symmetric_difference import (
    set_symmetric_difference,
)


def test_get_unique_elements_across_sets_two_sets() -> None:
    """
    Test case 1: Get unique elements across two sets.
    """
    set1 = {1, 2, 3}
    set2 = {2, 3, 4}
    result = get_unique_elements_across_sets(set1, set2)
    expected = [1, 4]  # Elements in exactly one set
    assert set(result) == set(expected)  # Order may vary


def test_get_unique_elements_across_sets_three_sets() -> None:
    """
    Test case 2: Get unique elements across three sets.
    """
    set1 = {1, 2, 3}
    set2 = {2, 3, 4}
    set3 = {3, 4, 5}
    result = get_unique_elements_across_sets(set1, set2, set3)
    expected = [1, 3, 5]  # Elements appearing in an odd number of sets
    assert set(result) == set(expected)


def test_get_unique_elements_across_sets_no_unique() -> None:
    """
    Test case 3: No unique elements (all elements appear in multiple sets).
    """
    set1 = {1, 2, 3}
    set2 = {1, 2, 3}
    set3 = {1, 2, 3}
    result = get_unique_elements_across_sets(set1, set2, set3)
    expected = [1, 2, 3]  # All elements appear in all sets (odd number)
    assert set(result) == set(expected)


def test_get_unique_elements_across_sets_all_unique() -> None:
    """
    Test case 4: All elements are unique.
    """
    set1 = {1, 2}
    set2 = {3, 4}
    set3 = {5, 6}
    result = get_unique_elements_across_sets(set1, set2, set3)
    expected = [1, 2, 3, 4, 5, 6]
    assert set(result) == set(expected)


def test_get_unique_elements_across_sets_strings() -> None:
    """
    Test case 5: Get unique elements with string sets.
    """
    set1 = {"a", "b", "c"}
    set2 = {"b", "c", "d"}
    result = get_unique_elements_across_sets(set1, set2)
    expected = ["a", "d"]
    assert set(result) == set(expected)


def test_get_unique_elements_across_sets_mixed_types() -> None:
    """
    Test case 6: Get unique elements with mixed types.
    """
    set1 = {1, "a", 3.14}
    set2 = {1, "b", 2.71}
    result = get_unique_elements_across_sets(set1, set2)
    expected = ["a", 3.14, "b", 2.71]
    assert set(result) == set(expected)


def test_set_symmetric_difference_two_sets() -> None:
    """
    Test case 7: Symmetric difference of two sets.
    """
    set1 = {1, 2, 3}
    set2 = {2, 3, 4}
    result = set_symmetric_difference(set1, set2)
    expected = {1, 4}
    assert result == expected


def test_set_symmetric_difference_three_sets() -> None:
    """
    Test case 8: Symmetric difference of three sets.
    """
    set1 = {1, 2, 3}
    set2 = {2, 3, 4}
    set3 = {3, 4, 5}
    result = set_symmetric_difference(set1, set2, set3)
    expected = {1, 3, 5}
    assert result == expected


def test_set_symmetric_difference_identical_sets() -> None:
    """
    Test case 9: Symmetric difference of identical sets.
    """
    set1 = {1, 2, 3}
    set2 = {1, 2, 3}
    set3 = {1, 2, 3}
    result = set_symmetric_difference(set1, set2, set3)
    expected = {1, 2, 3}
    assert result == expected


def test_set_symmetric_difference_empty_sets() -> None:
    """
    Test case 10: Symmetric difference including empty sets.
    """
    set1 = {1, 2, 3}
    set2 = set()
    result = set_symmetric_difference(set1, set2)
    assert result == {1, 2, 3}


def test_get_unique_elements_across_sets_type_error() -> None:
    """
    Test case 11: TypeError for non-set arguments.
    """
    with pytest.raises(TypeError, match="All arguments must be sets"):
        get_unique_elements_across_sets({1, 2}, "not a set")


def test_get_unique_elements_across_sets_value_error() -> None:
    """
    Test case 12: ValueError for fewer than 2 sets.
    """
    with pytest.raises(ValueError, match="At least 2 sets must be provided"):
        get_unique_elements_across_sets({1, 2})


def test_get_unique_elements_across_sets_four_sets_iteration() -> None:
    """Test case 13: Test with four sets to exercise full iteration logic."""
    result = get_unique_elements_across_sets({1, 2, 3}, {2, 3, 4}, {3, 4, 5}, {4, 5, 6})
    # Elements unique across all symmetric differences
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_unique_elements_across_sets_mixed_type_error_position() -> None:
    """Test case 14: TypeError with specific position for non-set at different positions."""
    with pytest.raises(TypeError, match="got list at position 1"):
        get_unique_elements_across_sets({1, 2}, [3, 4], {5, 6})


def test_set_symmetric_difference_type_error() -> None:
    """
    Test case 15: TypeError for non-set arguments.
    """
    with pytest.raises(TypeError, match="All arguments must be sets"):
        set_symmetric_difference({1, 2}, [3, 4])


def test_set_symmetric_difference_value_error() -> None:
    """
    Test case 16: ValueError for fewer than 2 sets.
    """
    with pytest.raises(ValueError, match="At least 2 sets must be provided"):
        set_symmetric_difference({1, 2})
