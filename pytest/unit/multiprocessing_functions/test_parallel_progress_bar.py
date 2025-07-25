import pytest
from multiprocessing_functions.parallel_progress_bar import parallel_progress_bar


def square(x: int) -> int:
    return x * x


def add_one(x: int) -> int:
    return x + 1


def test_parallel_progress_bar_basic() -> None:
    """Test progress bar parallel execution."""
    # Test case 1: Basic progress bar
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_progress_bar(square, data)
    assert result == [1, 4, 9]


def test_parallel_progress_bar_custom_processes() -> None:
    """Test progress bar with custom num_processes."""
    # Test case 2: Custom num_processes
    data: list[int] = [1, 2, 3]
    result: list[int] = parallel_progress_bar(add_one, data, num_processes=2)
    assert result == [2, 3, 4]
