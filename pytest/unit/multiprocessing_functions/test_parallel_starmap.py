import pytest
from multiprocessing_functions.parallel_starmap import parallel_starmap

def multiply(a: int, b: int) -> int:
    return a * b

def add(a: int, b: int) -> int:
    return a + b


def test_parallel_starmap_basic() -> None:
    """Test parallel_starmap multiplying pairs of numbers."""
    # Test case 1: Basic starmap
    data: list[tuple[int, int]] = [(1, 2), (3, 4), (5, 6)]
    result: list[int] = parallel_starmap(multiply, data)
    assert result == [2, 12, 30]


def test_parallel_starmap_empty() -> None:
    """Test parallel_starmap with an empty list."""
    # Test case 2: Empty data
    data: list[tuple[int, int]] = []
    result: list[int] = parallel_starmap(add, data)
    assert result == []
