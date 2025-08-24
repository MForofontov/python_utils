from multiprocessing_functions.parallel_unique import parallel_unique


def test_parallel_unique_basic() -> None:
    """
    Test case 1: Test extracting unique elements from a list.
    """
    data: list[int] = [1, 2, 2, 3, 3, 4]
    result: list[int] = parallel_unique(data)
    assert sorted(result) == [1, 2, 3, 4]


def test_parallel_unique_chunk_size() -> None:
    """
    Test case 2: Test parallel_unique with a custom chunk size.
    """
    data: list[int] = [1, 1, 2, 2, 3]
    result: list[int] = parallel_unique(data, chunk_size=2)
    assert sorted(result) == [1, 2, 3]
