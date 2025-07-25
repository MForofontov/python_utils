import pytest
from multiprocessing_functions.parallel_apply_with_args import parallel_apply_with_args


def add_offset(x: int, offset: int) -> int:
    return x + offset


def test_parallel_apply_with_args_basic() -> None:
    """Test parallel_apply_with_args with an additional argument."""
    # Test case 1: Basic usage with offset
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_apply_with_args(
        add_offset, data, args=(10,), num_processes=2
    )
    assert result == [11, 12, 13]


def test_parallel_apply_with_args_empty_data() -> None:
    """Test parallel_apply_with_args with an empty list."""
    # Test case 2: Empty data list
    data: list[int] = []
    result: list[int] = parallel_apply_with_args(add_offset, data, args=(5,))
    assert result == []
