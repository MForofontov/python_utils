import pytest
from multiprocessing_functions.parallel_broadcast import parallel_broadcast

def multiply_shared(x: int, shared: int) -> int:
    return x * shared

def add_shared(x: int, shared: int) -> int:
    return x + shared


def test_parallel_broadcast_basic() -> None:
    """Test parallel_broadcast with shared multiplication."""
    # Test case 1: Basic broadcast
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_broadcast(multiply_shared, 2, data)
    assert result == [2, 4, 6]


def test_parallel_broadcast_custom_processes() -> None:
    """Test parallel_broadcast with a custom process count."""
    # Test case 2: Custom num_processes
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_broadcast(add_shared, 5, data, num_processes=2)
    assert result == [6, 7, 8]


def test_parallel_broadcast_empty_data() -> None:
    """Test parallel_broadcast with an empty list."""
    # Test case 3: Empty data list
    data: list[int] = []
    result: list[int] = parallel_broadcast(multiply_shared, 2, data)
    assert result == []
