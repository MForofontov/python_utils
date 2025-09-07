import pytest
from typing import Any
from iterable_functions.list_operations.sliding_window import sliding_window


def test_sliding_window_normal_case() -> None:
    """
    Test case 1: Normal operation with window size 3.
    """
    items = [1, 2, 3, 4, 5]
    result = list(sliding_window(items, 3))
    expected = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    assert result == expected


def test_sliding_window_window_size_1() -> None:
    """
    Test case 2: Window size 1.
    """
    items = ["a", "b", "c"]
    result = list(sliding_window(items, 1))
    expected = [["a"], ["b"], ["c"]]
    assert result == expected


def test_sliding_window_window_size_equals_length() -> None:
    """
    Test case 3: Window size equals list length.
    """
    items = [1, 2, 3]
    result = list(sliding_window(items, 3))
    expected = [[1, 2, 3]]
    assert result == expected


def test_sliding_window_empty_list() -> None:
    """
    Test case 4: Empty list.
    """
    items = []
    result = list(sliding_window(items, 2))
    expected = []
    assert result == expected


def test_sliding_window_type_error_items() -> None:
    """
    Test case 5: TypeError for non-list items.
    """
    with pytest.raises(TypeError, match="items must be a list"):
        list(sliding_window("not a list", 2))


def test_sliding_window_type_error_window_size() -> None:
    """
    Test case 6: TypeError for non-int window_size.
    """
    with pytest.raises(TypeError, match="window_size must be an int"):
        list(sliding_window([1, 2, 3], "not an int"))


def test_sliding_window_value_error_window_size_zero() -> None:
    """
    Test case 7: ValueError for window_size 0.
    """
    with pytest.raises(ValueError, match="window_size must be at least 1"):
        list(sliding_window([1, 2, 3], 0))


def test_sliding_window_value_error_negative_window_size() -> None:
    """
    Test case 8: ValueError for negative window_size.
    """
    with pytest.raises(ValueError, match="window_size must be at least 1"):
        list(sliding_window([1, 2, 3], -1))


def test_sliding_window_boundary_window_larger_than_list() -> None:
    """
    Test case 9: Window size larger than list.
    """
    items = [1, 2]
    result = list(sliding_window(items, 5))
    expected = []
    assert result == expected


def test_sliding_window_large_list() -> None:
    """
    Test case 10: Performance test with large list.
    """
    items = list(range(1000))
    result = list(sliding_window(items, 10))
    assert len(result) == 991  # 1000 - 10 + 1
    assert result[0] == list(range(10))
    assert result[-1] == list(range(990, 1000))
