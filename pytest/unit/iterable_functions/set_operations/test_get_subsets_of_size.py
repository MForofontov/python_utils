import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from iterable_functions.set_operations.get_subsets_of_size import get_subsets_of_size


def test_get_subsets_of_size_normal_case() -> None:
    """
    Test case 1: Get subsets of size 2 from a set.
    """
    input_set = {1, 2, 3, 4}
    size = 2
    result = get_subsets_of_size(input_set, size)
    expected = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    assert result == expected


def test_get_subsets_of_size_size_3() -> None:
    """
    Test case 2: Get subsets of size 3.
    """
    input_set = {1, 2, 3, 4}
    size = 3
    result = get_subsets_of_size(input_set, size)
    expected = [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
    assert result == expected


def test_get_subsets_of_size_size_0() -> None:
    """
    Test case 3: Get subsets of size 0 (empty subsets).
    """
    input_set = {1, 2, 3}
    size = 0
    expected = [[]]
    result = get_subsets_of_size(input_set, size)
    assert result == expected


def test_get_subsets_of_size_size_equals_n() -> None:
    """
    Test case 4: Get subsets of size equal to set size.
    """
    input_set = {1, 2, 3}
    size = 3
    expected = [[1, 2, 3]]
    result = get_subsets_of_size(input_set, size)
    assert result == expected


def test_get_subsets_of_size_empty_set() -> None:
    """
    Test case 5: Get subsets from empty set.
    """
    input_set = set()
    size = 0
    expected = [[]]
    result = get_subsets_of_size(input_set, size)
    assert result == expected


def test_get_subsets_of_size_single_element() -> None:
    """
    Test case 6: Get subsets from single element set.
    """
    input_set = {1}
    size = 1
    expected = [[1]]
    result = get_subsets_of_size(input_set, size)
    assert result == expected


def test_get_subsets_of_size_strings() -> None:
    """
    Test case 7: Get subsets with string elements.
    """
    input_set = {"a", "b", "c"}
    size = 2
    result = get_subsets_of_size(input_set, size)
    expected = [["a", "b"], ["a", "c"], ["b", "c"]]
    assert result == expected


def test_get_subsets_of_size_mixed_types() -> None:
    """
    Test case 8: Get subsets with mixed types.
    """
    input_set = {1, "a", 3.14}
    size = 2
    result = get_subsets_of_size(input_set, size)
    assert len(result) == 3  # C(3,2) = 3
    # Check that all subsets have correct size
    assert all(len(subset) == 2 for subset in result)


def test_get_subsets_of_size_boundary_size_1() -> None:
    """
    Test case 9: Boundary test with size=1.
    """
    input_set = {1, 2, 3}
    size = 1
    result = get_subsets_of_size(input_set, size)
    expected = [[1], [2], [3]]
    assert result == expected


def test_get_subsets_of_size_type_error_input_set() -> None:
    """
    Test case 10: TypeError for invalid input_set type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        get_subsets_of_size("not a set", 2)


def test_get_subsets_of_size_type_error_size() -> None:
    """
    Test case 11: TypeError for invalid size type.
    """
    input_set = {1, 2, 3}
    with pytest.raises(TypeError, match="size must be an int"):
        get_subsets_of_size(input_set, "not an int")


def test_get_subsets_of_size_value_error_negative_size() -> None:
    """
    Test case 12: ValueError for negative size.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="size must be non-negative"):
        get_subsets_of_size(input_set, -1)


def test_get_subsets_of_size_value_error_size_too_large() -> None:
    """
    Test case 13: ValueError for size larger than set size.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="size cannot be larger than set size 3"):
        get_subsets_of_size(input_set, 4)
