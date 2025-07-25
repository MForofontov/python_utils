import pytest
from multiprocessing_functions.parallel_map import parallel_map


def square(x: int) -> int:
    return x * x


def add_one(x: int) -> int:
    return x + 1


def test_parallel_map_basic() -> None:
    """Test the parallel_map function with a simple square function."""
    # Test case 1: Basic square mapping
    data: list[int] = [1, 2, 3, 4]
    result: list[int] = parallel_map(square, data)
    assert result == [1, 4, 9, 16]


def test_parallel_map_custom_processes() -> None:
    """Test the parallel_map function with a specific number of processes."""
    # Test case 2: Custom num_processes
    data: list[int] = [1, 2, 3, 4]
    result: list[int] = parallel_map(add_one, data, num_processes=2)
    assert result == [2, 3, 4, 5]


def test_parallel_map_empty_list() -> None:
    """Test the parallel_map function with an empty list."""
    # Test case 3: Empty list
    data: list[int] = []
    result: list[int] = parallel_map(square, data)
    assert result == []
