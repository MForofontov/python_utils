from multiprocessing_functions.parallel_unique import parallel_unique


def test_parallel_unique_basic() -> None:
    """Test extracting unique elements from a list."""
    # Test case 1: Basic unique
    data: list[int] = [1, 2, 2, 3, 3, 4]
    result: list[int] = parallel_unique(data)
    assert sorted(result) == [1, 2, 3, 4]


def test_parallel_unique_chunk_size() -> None:
    """Test parallel_unique with a custom chunk size."""
    # Test case 2: Custom chunk size
    data: list[int] = [1, 1, 2, 2, 3]
    result: list[int] = parallel_unique(data, chunk_size=2)
    assert sorted(result) == [1, 2, 3]
