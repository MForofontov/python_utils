from multiprocessing_functions.parallel_sum import parallel_sum


def test_parallel_sum_basic() -> None:
    """Test summing a list of integers."""
    # Test case 1: Basic sum
    data: list[int] = [1, 2, 3, 4]
    result: int = parallel_sum(data)
    assert result == 10


def test_parallel_sum_chunk_size() -> None:
    """Test parallel_sum with a specific chunk size."""
    # Test case 2: Custom chunk size
    data: list[int] = [1, 2, 3, 4]
    result: int = parallel_sum(data, chunk_size=2)
    assert result == 10
