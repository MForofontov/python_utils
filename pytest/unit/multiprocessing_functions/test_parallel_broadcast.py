import pytest

pytestmark = [pytest.mark.unit, pytest.mark.multiprocessing_functions]
from python_utils.multiprocessing_functions.parallel_broadcast import parallel_broadcast


def multiply_shared(x: int, shared: int) -> int:
    return x * shared


def add_shared(x: int, shared: int) -> int:
    return x + shared


def test_parallel_broadcast_basic() -> None:
    """
    Test case 1: Test parallel_broadcast with shared multiplication.
    """
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_broadcast(multiply_shared, 2, data)
    assert result == [2, 4, 6]


def test_parallel_broadcast_custom_processes() -> None:
    """
    Test case 2: Test parallel_broadcast with a custom process count.
    """
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_broadcast(add_shared, 5, data, num_processes=2)
    assert result == [6, 7, 8]


def test_parallel_broadcast_empty_data() -> None:
    """
    Test case 3: Test parallel_broadcast with an empty list.
    """
    data: list[int] = []
    result: list[int] = parallel_broadcast(multiply_shared, 2, data)
    assert result == []
