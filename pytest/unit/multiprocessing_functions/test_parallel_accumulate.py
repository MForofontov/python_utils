import pytest

pytestmark = [pytest.mark.unit, pytest.mark.multiprocessing_functions]
from pyutils_collection.multiprocessing_functions.parallel_accumulate import parallel_accumulate


def add(a: int, b: int) -> int:
    return a + b


def test_parallel_accumulate_basic() -> None:
    """
    Test case 1: Test parallel_accumulate with a simple addition function.
    """
    data: list[int] = [1, 2, 3, 4]
    result: list[int] = parallel_accumulate(add, data)
    assert result == [1, 3, 6, 10]


def test_parallel_accumulate_chunk_size() -> None:
    """
    Test case 2: Test parallel_accumulate with a custom chunk size.
    """
    data: list[int] = [1, 2, 3, 4]
    result: list[int] = parallel_accumulate(add, data, chunk_size=2)
    assert result == [1, 3, 6, 10]


def test_parallel_accumulate_empty() -> None:
    """
    Test case 3: Test parallel_accumulate with an empty list.
    """
    data: list[int] = []
    result: list[int] = parallel_accumulate(add, data)
    assert result == []
