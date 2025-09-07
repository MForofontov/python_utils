import pytest
from typing import Any
from iterable_functions.set_operations.partition_set_by_sizes import partition_set_by_sizes


def test_partition_set_by_sizes_normal_case() -> None:
    """
    Test case 1: Normal operation with two partitions.
    """
    input_set = {1, 2, 3, 4, 5}
    sizes = [2, 3]
    result = partition_set_by_sizes(input_set, sizes)

    assert len(result) == 2
    assert len(result[0]) == 2
    assert len(result[1]) == 3
    # All elements should be in exactly one partition
    all_elements = set()
    for partition in result:
        all_elements.update(partition)
    assert all_elements == input_set


def test_partition_set_by_sizes_three_partitions() -> None:
    """
    Test case 2: Three partitions.
    """
    input_set = {'a', 'b', 'c', 'd', 'e', 'f'}
    sizes = [1, 2, 3]
    result = partition_set_by_sizes(input_set, sizes)

    assert len(result) == 3
    assert len(result[0]) == 1
    assert len(result[1]) == 2
    assert len(result[2]) == 3


def test_partition_set_by_sizes_single_partition() -> None:
    """
    Test case 3: Single partition.
    """
    input_set = {1, 2, 3}
    sizes = [3]
    result = partition_set_by_sizes(input_set, sizes)

    assert len(result) == 1
    assert result[0] == input_set


def test_partition_set_by_sizes_type_error_input_set() -> None:
    """
    Test case 4: TypeError for non-set input_set.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        partition_set_by_sizes([1, 2, 3], [2, 1])


def test_partition_set_by_sizes_type_error_sizes() -> None:
    """
    Test case 5: TypeError for non-list sizes.
    """
    with pytest.raises(TypeError, match="sizes must be a list"):
        partition_set_by_sizes({1, 2, 3}, "not a list")


def test_partition_set_by_sizes_type_error_sizes_elements() -> None:
    """
    Test case 6: TypeError for non-int sizes elements.
    """
    with pytest.raises(TypeError, match="All sizes must be integers"):
        partition_set_by_sizes({1, 2, 3}, [2, "not int"])


def test_partition_set_by_sizes_value_error_negative_size() -> None:
    """
    Test case 7: ValueError for negative size.
    """
    with pytest.raises(ValueError, match="All sizes must be positive"):
        partition_set_by_sizes({1, 2, 3}, [2, -1])


def test_partition_set_by_sizes_value_error_zero_size() -> None:
    """
    Test case 8: ValueError for zero size.
    """
    with pytest.raises(ValueError, match="All sizes must be positive"):
        partition_set_by_sizes({1, 2, 3}, [2, 0])


def test_partition_set_by_sizes_value_error_wrong_sum() -> None:
    """
    Test case 9: ValueError for sizes sum not equal to set size.
    """
    with pytest.raises(ValueError, match="Sum of sizes .* must equal set size"):
        partition_set_by_sizes({1, 2, 3}, [2, 3])


def test_partition_set_by_sizes_boundary_empty_set() -> None:
    """
    Test case 10: Empty set with empty sizes.
    """
    input_set = set()
    sizes = []
    result = partition_set_by_sizes(input_set, sizes)
    assert result == []


def test_partition_set_by_sizes_large_set() -> None:
    """
    Test case 11: Performance test with large set.
    """
    input_set = set(range(1000))
    sizes = [300, 400, 300]
    result = partition_set_by_sizes(input_set, sizes)

    assert len(result) == 3
    assert len(result[0]) == 300
    assert len(result[1]) == 400
    assert len(result[2]) == 300
