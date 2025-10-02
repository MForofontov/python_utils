import pytest
from iterable_functions.set_operations.get_set_partitions import get_set_partitions


def test_get_set_partitions_three_elements_two_parts() -> None:
    """
    Test case 1: Partition {1,2,3} into 2 subsets.
    """
    input_set = {1, 2, 3}
    k = 2
    result = get_set_partitions(input_set, k)
    valid_partitions = [p for p in result if len(p) == k]
    assert valid_partitions, "No valid partitions with k subsets found"
    # Each subset should be non-empty
    for partition in valid_partitions:
        assert all(len(subset) > 0 for subset in partition)
    # Union of each partition should equal original set
    for partition in valid_partitions:
        union = set()
        for subset in partition:
            union.update(subset)
        assert union == input_set


def test_get_set_partitions_three_elements_three_parts() -> None:
    """
    Test case 2: Partition {1,2,3} into 3 subsets.
    """
    input_set = {1, 2, 3}
    k = 3
    result = get_set_partitions(input_set, k)
    valid_partitions = [p for p in result if len(p) == k]
    assert valid_partitions, "No valid partitions with k subsets found"
    for partition in valid_partitions:
        assert all(len(subset) > 0 for subset in partition)
        union = set()
        for subset in partition:
            union.update(subset)
        assert union == input_set


def test_get_set_partitions_four_elements_two_parts() -> None:
    """
    Test case 3: Partition {1,2,3,4} into 2 subsets.
    """
    input_set = {1, 2, 3, 4}
    k = 2
    result = get_set_partitions(input_set, k)
    valid_partitions = [p for p in result if len(p) == k]
    assert valid_partitions, "No valid partitions with k subsets found"
    for partition in valid_partitions:
        assert all(len(subset) > 0 for subset in partition)
        union = set()
        for subset in partition:
            union.update(subset)
        assert union == input_set


def test_get_set_partitions_single_element() -> None:
    """
    Test case 4: Partition single element set.
    """
    input_set = {1}
    k = 1
    result = get_set_partitions(input_set, k)
    assert len(result) == 1
    assert result[0] == [{1}]


def test_get_set_partitions_empty_set() -> None:
    """
    Test case 5: Partition empty set.
    """
    input_set = set()
    k = 1
    with pytest.raises(ValueError, match="k cannot be greater than set size 0"):
        get_set_partitions(input_set, k)


def test_get_set_partitions_strings() -> None:
    """
    Test case 6: Partition set with string elements.
    """
    input_set = {"a", "b"}
    k = 2
    result = get_set_partitions(input_set, k)
    valid_partitions = [p for p in result if len(p) == k]
    assert valid_partitions, "No valid partitions with k subsets found"
    for partition in valid_partitions:
        assert all(len(subset) > 0 for subset in partition)
        union = set()
        for subset in partition:
            union.update(subset)
        assert union == input_set


def test_get_set_partitions_type_error_input_set() -> None:
    """
    Test case 7: TypeError for invalid input_set type.
    """
    with pytest.raises(TypeError, match="input_set must be a set"):
        get_set_partitions("not a set", 2)


def test_get_set_partitions_type_error_k() -> None:
    """
    Test case 8: TypeError for invalid k type.
    """
    input_set = {1, 2, 3}
    with pytest.raises(TypeError, match="k must be an int"):
        get_set_partitions(input_set, "not an int")


def test_get_set_partitions_value_error_k_zero() -> None:
    """
    Test case 9: ValueError for k=0.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="k must be at least 1"):
        get_set_partitions(input_set, 0)


def test_get_set_partitions_value_error_k_negative() -> None:
    """
    Test case 10: ValueError for negative k.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="k must be at least 1"):
        get_set_partitions(input_set, -1)


def test_get_set_partitions_value_error_k_too_large() -> None:
    """
    Test case 11: ValueError for k larger than set size.
    """
    input_set = {1, 2, 3}
    with pytest.raises(ValueError, match="k cannot be greater than set size 3"):
        get_set_partitions(input_set, 4)


def test_get_set_partitions_no_duplicates() -> None:
    """
    Test case 12: Ensure no duplicate partitions are returned.
    """
    input_set = {1, 2, 3, 4}
    k = 2
    result = get_set_partitions(input_set, k)
    # Convert to set of frozensets for uniqueness check
    unique_check = set()
    for partition in result:
        partition_hash = frozenset(frozenset(s) for s in partition)
        assert partition_hash not in unique_check
        unique_check.add(partition_hash)
