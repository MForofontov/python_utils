from multiprocessing_functions.parallel_sum import parallel_sum


def test_parallel_sum_basic() -> None:
    """
    Test case 1: Test summing a list of integers.
    """
    data: list[int] = [1, 2, 3, 4]
    result: int = parallel_sum(data)
    assert result == 10


def test_parallel_sum_chunk_size() -> None:
    """
    Test case 2: Test parallel_sum with a specific chunk size.
    """
    data: list[int] = [1, 2, 3, 4]
    result: int = parallel_sum(data, chunk_size=2)
    assert result == 10
