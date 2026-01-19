import pytest

pytestmark = [pytest.mark.unit, pytest.mark.multiprocessing_functions]
from multiprocessing_functions.parallel_apply_with_args import parallel_apply_with_args


def add_offset(x: int, offset: int) -> int:
    return x + offset


def test_parallel_apply_with_args_basic() -> None:
    """
    Test case 1: Test parallel_apply_with_args with an additional argument.
    """
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_apply_with_args(
        add_offset, data, args=(10,), num_processes=2
    )
    assert result == [11, 12, 13]


def test_parallel_apply_with_args_empty_data() -> None:
    """
    Test case 2: Test parallel_apply_with_args with an empty list.
    """
    data: list[int] = []
    result: list[int] = parallel_apply_with_args(add_offset, data, args=(5,))
    assert result == []
