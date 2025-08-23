from multiprocessing_functions.parallel_filter import parallel_filter


def is_even(x: int) -> bool:
    return x % 2 == 0


def greater_than_two(x: int) -> bool:
    return x > 2


def test_parallel_filter_basic() -> None:
    """Test parallel_filter to keep even numbers."""
    # Test case 1: Filter even numbers
    data: list[int] = [1, 2, 3, 4, 5, 6]
    result: list[int] = parallel_filter(is_even, data)
    assert result == [2, 4, 6]


def test_parallel_filter_custom_processes() -> None:
    """Test parallel_filter with custom num_processes."""
    # Test case 2: Custom num_processes
    data: list[int] = [1, 2, 3, 4]
    result: list[int] = parallel_filter(
        greater_than_two, data, num_processes=2)
    assert result == [3, 4]


def test_parallel_filter_empty() -> None:
    """Test parallel_filter with an empty list."""
    # Test case 3: Empty list
    data: list[int] = []
    result: list[int] = parallel_filter(is_even, data)
    assert result == []
