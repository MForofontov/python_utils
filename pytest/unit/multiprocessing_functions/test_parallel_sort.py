from multiprocessing_functions.parallel_sort import parallel_sort


def test_parallel_sort_basic() -> None:
    """Test parallel_sort on an unsorted list."""
    # Test case 1: Basic sorting
    data: list[int] = [5, 2, 3, 1, 4]
    result: list[int] = parallel_sort(data)
    assert result == [1, 2, 3, 4, 5]


def test_parallel_sort_chunk_size() -> None:
    """Test parallel_sort with a specific chunk size."""
    # Test case 2: Custom chunk size
    data: list[int] = [4, 3, 2, 1]
    result: list[int] = parallel_sort(data, chunk_size=2)
    assert result == [1, 2, 3, 4]
