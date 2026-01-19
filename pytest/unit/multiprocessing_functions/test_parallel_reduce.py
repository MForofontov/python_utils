import pytest

pytestmark = [pytest.mark.unit, pytest.mark.multiprocessing_functions]
from python_utils.multiprocessing_functions.parallel_reduce import parallel_reduce


def add(a: int, b: int) -> int:
    return a + b


def test_parallel_reduce_basic() -> None:
    """
    Test case 1: Test parallel_reduce summing numbers.
    """
    data: list[int] = [1, 2, 3, 4]
    result: int = parallel_reduce(add, data)
    assert result == 10


def test_parallel_reduce_chunk_size() -> None:
    """
    Test case 2: Test parallel_reduce with a custom chunk size.
    """
    data: list[int] = [1, 2, 3, 4]
    result: int = parallel_reduce(add, data, chunk_size=2)
    assert result == 10
