import pytest

pytestmark = [pytest.mark.unit, pytest.mark.multiprocessing_functions]
from python_utils.multiprocessing_functions.parallel_pipeline import parallel_pipeline


def square(x: int) -> int:
    return x * x


def add_one(x: int) -> int:
    return x + 1


def double(x: int) -> int:
    return x * 2


def test_parallel_pipeline_basic() -> None:
    """
    Test case 1: Test pipeline of squaring then adding one.
    """
    funcs = [square, add_one]
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_pipeline(funcs, data)
    assert result == [2, 5, 10]


def test_parallel_pipeline_empty() -> None:
    """
    Test case 2: Test pipeline with empty data list.
    """
    funcs = [double]
    data: list[int] = []
    result: list[int] = parallel_pipeline(funcs, data)
    assert result == []
