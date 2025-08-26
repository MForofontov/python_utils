from multiprocessing_functions.parallel_sum import parallel_sum
import pytest


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


def test_parallel_sum_empty_list() -> None:
    """
    Test case 3: Test parallel_sum with empty list.
    """
    data: list[int] = []
    result: int = parallel_sum(data)
    assert result == 0


def test_parallel_sum_single_element() -> None:
    """
    Test case 4: Test parallel_sum with single element.
    """
    data: list[int] = [42]
    result: int = parallel_sum(data)
    assert result == 42


def test_parallel_sum_negative_numbers() -> None:
    """
    Test case 5: Test parallel_sum with negative numbers.
    """
    data: list[int] = [-5, -3, 2, 8, -1]
    result: int = parallel_sum(data)
    assert result == 1


def test_parallel_sum_large_list() -> None:
    """
    Test case 6: Test parallel_sum with larger list.
    """
    data: list[int] = list(range(1, 101))  # [1, 2, ..., 100]
    result: int = parallel_sum(data)
    assert result == 5050  # Sum of 1 to 100


def test_parallel_sum_zeros() -> None:
    """
    Test case 7: Test parallel_sum with zeros.
    """
    data: list[int] = [0, 0, 0, 0]
    result: int = parallel_sum(data)
    assert result == 0


def test_parallel_sum_custom_processes() -> None:
    """
    Test case 8: Test parallel_sum with custom number of processes.
    """
    data: list[int] = [1, 2, 3, 4, 5, 6]
    result: int = parallel_sum(data, num_processes=2)
    assert result == 21


def test_parallel_sum_invalid_data_type() -> None:
    """
    Test case 9: Test parallel_sum with invalid data type.
    """
    with pytest.raises(TypeError):
        parallel_sum("not_a_list")


def test_parallel_sum_invalid_num_processes_type() -> None:
    """
    Test case 10: Test parallel_sum with invalid num_processes type.
    """
    with pytest.raises(TypeError):
        parallel_sum([1, 2, 3], num_processes="invalid")


def test_parallel_sum_invalid_chunk_size_type() -> None:
    """
    Test case 11: Test parallel_sum with invalid chunk_size type.
    """
    with pytest.raises(TypeError):
        parallel_sum([1, 2, 3], chunk_size="invalid")


def test_parallel_sum_zero_chunk_size() -> None:
    """
    Test case 12: Test parallel_sum with zero chunk_size.
    """
    with pytest.raises(ValueError):
        parallel_sum([1, 2, 3], chunk_size=0)


def test_parallel_sum_negative_chunk_size() -> None:
    """
    Test case 13: Test parallel_sum with negative chunk_size.
    """
    with pytest.raises(ValueError):
        parallel_sum([1, 2, 3], chunk_size=-1)


def test_parallel_sum_zero_num_processes() -> None:
    """
    Test case 14: Test parallel_sum with zero num_processes.
    """
    with pytest.raises(ValueError):
        parallel_sum([1, 2, 3], num_processes=0)


def test_parallel_sum_negative_num_processes() -> None:
    """
    Test case 15: Test parallel_sum with negative num_processes.
    """
    with pytest.raises(ValueError):
        parallel_sum([1, 2, 3], num_processes=-1)
