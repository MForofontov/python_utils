import pytest
from iterable_functions.list_operations.find_duplicates import find_duplicates


def test_find_duplicates_normal_case() -> None:
    """
    Test case 1: Normal operation with duplicates.
    """
    items = [1, 2, 2, 3, 3, 3, 4]
    expected = {2: 2, 3: 3}
    result = find_duplicates(items)
    assert result == expected


def test_find_duplicates_no_duplicates() -> None:
    """
    Test case 2: No duplicates in the list.
    """
    items = [1, 2, 3, 4]
    expected = {}
    result = find_duplicates(items)
    assert result == expected


def test_find_duplicates_empty_list() -> None:
    """
    Test case 3: Empty list.
    """
    items = []
    expected = {}
    result = find_duplicates(items)
    assert result == expected


def test_find_duplicates_strings() -> None:
    """
    Test case 4: String elements with duplicates.
    """
    items = ["apple", "banana", "apple", "cherry", "banana"]
    expected = {"apple": 2, "banana": 2}
    result = find_duplicates(items)
    assert result == expected


def test_find_duplicates_type_error() -> None:
    """
    Test case 5: TypeError for non-list input.
    """
    with pytest.raises(TypeError, match="items must be a list"):
        find_duplicates("not a list")


def test_find_duplicates_boundary_single_element() -> None:
    """
    Test case 6: Single element (no duplicates).
    """
    items = [42]
    expected = {}
    result = find_duplicates(items)
    assert result == expected


def test_find_duplicates_boundary_all_duplicates() -> None:
    """
    Test case 7: All elements are duplicates.
    """
    items = [1, 1, 1, 1]
    expected = {1: 4}
    result = find_duplicates(items)
    assert result == expected


def test_find_duplicates_large_list() -> None:
    """
    Test case 8: Performance test with large list.
    """
    items = list(range(1000)) + [999] * 5  # 999 appears 6 times total
    result = find_duplicates(items)
    assert 999 in result
    assert result[999] == 6
