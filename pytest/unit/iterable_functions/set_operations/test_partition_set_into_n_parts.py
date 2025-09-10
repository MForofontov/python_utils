import pytest
from iterable_functions.set_operations.partition_set_into_n_parts import partition_set_into_n_parts


def test_partition_set_into_n_parts_normal_case() -> None:
    """
    Test case 1: Partition a set into 3 parts.
    """
    input_set = {1, 2, 3, 4, 5, 6, 7}
    n = 3
    result = partition_set_into_n_parts(input_set, n)
    # Should have 3 partitions
    assert len(result) == 3
    # All partitions should be sets
    assert all(isinstance(p, set) for p in result)
    # Union of all partitions should equal original set
    union = set()
    for p in result:
        union.update(p)
    assert union == input_set
    # All partitions should be pairwise disjoint
    for i, p1 in enumerate(result):
        for p2 in result[i+1:]:
            assert len(p1 & p2) == 0


def test_partition_set_into_n_parts_two_parts() -> None:
    """
    Test case 2: Partition a set into 2 parts.
    """
    input_set = {1, 2, 3, 4, 5, 6}
    n = 2
    result = partition_set_into_n_parts(input_set, n)
    assert len(result) == 2
    # Check sizes are approximately equal
    sizes = [len(p) for p in result]
    assert abs(sizes[0] - sizes[1]) <= 1  # Difference should be at most 1


def test_partition_set_into_n_parts_single_partition() -> None:
    """
    Test case 3: Partition a set into 1 part.
    """
    input_set = {1, 2, 3, 4}
    n = 1
    result = partition_set_into_n_parts(input_set, n)
    assert len(result) == 1
    assert result[0] == input_set


def test_partition_set_into_n_parts_more_parts_than_elements() -> None:
    """
    Test case 4: More partitions than elements.
    """
    input_set = {1, 2, 3}
    n = 5
    result = partition_set_into_n_parts(input_set, n)
    assert len(result) == 5
    # First 3 partitions should have one element each
    assert len(result[0]) == 1
    assert len(result[1]) == 1
    assert len(result[2]) == 1
    # Last 2 partitions should be empty
    assert len(result[3]) == 0
    assert len(result[4]) == 0


def test_partition_set_into_n_parts_empty_set() -> None:
    """
    Test case 5: Partition empty set.
    """
    input_set = set()
    n = 3
    result = partition_set_into_n_parts(input_set, n)
    assert len(result) == 3
    assert all(len(p) == 0 for p in result)


def test_partition_set_into_n_parts_single_element() -> None:
    """
    Test case 6: Partition single element set.
    """
    input_set = {1}
    n = 2
    result = partition_set_into_n_parts(input_set, n)
    assert len(result) == 2
    assert len(result[0]) == 1
    assert len(result[1]) == 0
    assert result[0] == {1}


def test_partition_set_into_n_parts_strings() -> None:
    """
    Test case 7: Partition set with string elements.
    """
    input_set = {"a", "b", "c", "d"}
    n = 2
    result = partition_set_into_n_parts(input_set, n)
    assert len(result) == 2
    # Check union equals original
    union = set()
    for p in result:
        union.update(p)
    assert union == input_set


def test_partition_set_into_n_parts_type_error_input_set() -> None:
    """
    Test case 8: TypeError for invalid input_set type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        partition_set_into_n_parts("not a set", 2)


def test_partition_set_into_n_parts_type_error_n() -> None:
    """
    Test case 9: TypeError for invalid n type.
    """
    input_set = {1, 2, 3}
    with pytest.raises(TypeError, match="n must be an int"):
        partition_set_into_n_parts(input_set, "not an int")


def test_partition_set_into_n_parts_value_error_n_zero() -> None:
    """
    Test case 10: ValueError for n=0.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="n must be at least 1"):
        partition_set_into_n_parts(input_set, 0)


def test_partition_set_into_n_parts_value_error_n_negative() -> None:
    """
    Test case 11: ValueError for negative n.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="n must be at least 1"):
        partition_set_into_n_parts(input_set, -1)


def test_partition_set_into_n_parts_equal_distribution() -> None:
    """
    Test case 12: Test that elements are distributed evenly.
    """
    input_set = set(range(10))  # 10 elements
    n = 3
    result = partition_set_into_n_parts(input_set, n)
    sizes = [len(p) for p in result]
    # Should be [4, 3, 3] or similar distribution
    assert sum(sizes) == 10
    assert max(sizes) - min(sizes) <= 1
