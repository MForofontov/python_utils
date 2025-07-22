import pytest
from multiprocessing_functions.parallel_reduce import parallel_reduce

def add(a: int, b: int) -> int:
    return a + b


def test_parallel_reduce_basic() -> None:
    """Test parallel_reduce summing numbers."""
    # Test case 1: Basic sum reduction
    data: list[int] = [1, 2, 3, 4]
    result: int = parallel_reduce(add, data)
    assert result == 10


def test_parallel_reduce_chunk_size() -> None:
    """Test parallel_reduce with a custom chunk size."""
    # Test case 2: Custom chunk size
    data: list[int] = [1, 2, 3, 4]
    result: int = parallel_reduce(add, data, chunk_size=2)
    assert result == 10

