from multiprocessing_functions.parallel_accumulate import parallel_accumulate


def add(a: int, b: int) -> int:
    return a + b


def test_parallel_accumulate_basic() -> None:
    """Test parallel_accumulate with a simple addition function."""
    # Test case 1: Basic accumulate
    data: list[int] = [1, 2, 3, 4]
    result: list[int] = parallel_accumulate(add, data)
    assert result == [1, 3, 6, 10]


def test_parallel_accumulate_chunk_size() -> None:
    """Test parallel_accumulate with a custom chunk size."""
    # Test case 2: Custom chunk size
    data: list[int] = [1, 2, 3, 4]
    result: list[int] = parallel_accumulate(add, data, chunk_size=2)
    assert result == [1, 3, 6, 10]


def test_parallel_accumulate_empty() -> None:
    """Test parallel_accumulate with an empty list."""
    # Test case 3: Empty list
    data: list[int] = []
    result: list[int] = parallel_accumulate(add, data)
    assert result == []
