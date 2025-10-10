"""Unit tests for partition_set_by_predicate function."""

import pytest
from iterable_functions.set_operations.set_partition import partition_set_by_predicate


def test_partition_set_by_predicate_even_odd() -> None:
    """
    Test case 1: Partition numbers into even and odd.
    """
    # Arrange
    numbers = {1, 2, 3, 4, 5, 6}

    # Act
    even, odd = partition_set_by_predicate(numbers, lambda x: x % 2 == 0)

    # Assert
    assert even == {2, 4, 6}
    assert odd == {1, 3, 5}


def test_partition_set_by_predicate_string_length() -> None:
    """
    Test case 2: Partition strings by length.
    """
    # Arrange
    strings = {"apple", "banana", "cherry", "date"}

    # Act
    long_strings, short_strings = partition_set_by_predicate(
        strings, lambda s: len(s) > 5
    )

    # Assert
    assert long_strings == {"banana", "cherry"}
    assert short_strings == {"apple", "date"}


def test_partition_set_by_predicate_all_true() -> None:
    """
    Test case 3: All elements satisfy predicate.
    """
    # Arrange
    numbers = {2, 4, 6, 8}

    # Act
    true_set, false_set = partition_set_by_predicate(numbers, lambda x: x % 2 == 0)

    # Assert
    assert true_set == {2, 4, 6, 8}
    assert false_set == set()


def test_partition_set_by_predicate_all_false() -> None:
    """
    Test case 4: No elements satisfy predicate.
    """
    # Arrange
    numbers = {1, 3, 5, 7}

    # Act
    true_set, false_set = partition_set_by_predicate(numbers, lambda x: x % 2 == 0)

    # Assert
    assert true_set == set()
    assert false_set == {1, 3, 5, 7}


def test_partition_set_by_predicate_empty_set() -> None:
    """
    Test case 5: Empty set returns two empty sets.
    """
    # Arrange
    empty_set: set[int] = set()

    # Act
    true_set, false_set = partition_set_by_predicate(empty_set, lambda x: x > 0)

    # Assert
    assert true_set == set()
    assert false_set == set()


def test_partition_set_by_predicate_single_element_true() -> None:
    """
    Test case 6: Single element that satisfies predicate.
    """
    # Arrange
    single_set = {5}

    # Act
    true_set, false_set = partition_set_by_predicate(single_set, lambda x: x > 0)

    # Assert
    assert true_set == {5}
    assert false_set == set()


def test_partition_set_by_predicate_single_element_false() -> None:
    """
    Test case 7: Single element that doesn't satisfy predicate.
    """
    # Arrange
    single_set = {-5}

    # Act
    true_set, false_set = partition_set_by_predicate(single_set, lambda x: x > 0)

    # Assert
    assert true_set == set()
    assert false_set == {-5}


def test_partition_set_by_predicate_complex_predicate() -> None:
    """
    Test case 8: Complex predicate with multiple conditions.
    """
    # Arrange
    numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    # Act
    true_set, false_set = partition_set_by_predicate(
        numbers, lambda x: x % 2 == 0 and x > 5
    )

    # Assert
    assert true_set == {6, 8, 10}
    assert false_set == {1, 2, 3, 4, 5, 7, 9}


def test_partition_set_by_predicate_preserves_union() -> None:
    """
    Test case 9: Union of partitions equals original set.
    """
    # Arrange
    original_set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    # Act
    true_set, false_set = partition_set_by_predicate(original_set, lambda x: x % 3 == 0)

    # Assert
    assert true_set.union(false_set) == original_set
    assert true_set.intersection(false_set) == set()


def test_partition_set_by_predicate_mixed_types() -> None:
    """
    Test case 10: Partition set with mixed types.
    """
    # Arrange
    mixed_set = {1, "a", 2.5, None}

    # Act
    true_set, false_set = partition_set_by_predicate(
        mixed_set, lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
    )

    # Assert
    assert 1 in true_set
    assert 2.5 in true_set
    assert "a" in false_set
    assert True in false_set
    assert None in false_set


def test_partition_set_by_predicate_type_error_non_set() -> None:
    """
    Test case 11: TypeError when input_set is not a set.
    """
    # Arrange
    invalid_input = [1, 2, 3, 4]

    # Act & Assert
    with pytest.raises(TypeError, match="input_set must be a set"):
        partition_set_by_predicate(invalid_input, lambda x: x % 2 == 0)  # type: ignore


def test_partition_set_by_predicate_type_error_non_callable() -> None:
    """
    Test case 12: TypeError when predicate is not callable.
    """
    # Arrange
    numbers = {1, 2, 3}
    invalid_predicate = "not callable"

    # Act & Assert
    with pytest.raises(TypeError, match="predicate must be callable"):
        partition_set_by_predicate(numbers, invalid_predicate)  # type: ignore
