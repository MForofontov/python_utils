"""Unit tests for SegmentTree class."""
from data_types.segment_tree import SegmentTree


def test_segment_tree_build_simple_array() -> None:
    """
    Test case 1: Build segment tree from simple array.
    """
    # Arrange
    tree = SegmentTree()
    arr = [1, 2, 3, 4, 5]

    # Act
    tree.build(arr)

    # Assert
    assert tree.n == 5
    assert len(tree.tree) == 10


def test_segment_tree_query_full_range() -> None:
    """
    Test case 2: Query full range sum.
    """
    # Arrange
    tree = SegmentTree()
    arr = [1, 2, 3, 4, 5]
    tree.build(arr)

    # Act
    result = tree.query(0, 4)

    # Assert
    assert result == 15


def test_segment_tree_query_partial_range() -> None:
    """
    Test case 3: Query partial range sum.
    """
    # Arrange
    tree = SegmentTree()
    arr = [1, 2, 3, 4, 5]
    tree.build(arr)

    # Act
    result = tree.query(1, 3)

    # Assert
    assert result == 9  # 2 + 3 + 4


def test_segment_tree_update_single_element() -> None:
    """
    Test case 4: Update single element and query.
    """
    # Arrange
    tree = SegmentTree()
    arr = [1, 2, 3, 4, 5]
    tree.build(arr)

    # Act
    tree.update(2, 10)  # Change 3 to 10
    result = tree.query(0, 4)

    # Assert
    assert result == 22  # 1 + 2 + 10 + 4 + 5


def test_segment_tree_multiple_updates() -> None:
    """
    Test case 5: Multiple updates and queries.
    """
    # Arrange
    tree = SegmentTree()
    arr = [1, 2, 3, 4, 5]
    tree.build(arr)

    # Act
    tree.update(0, 5)
    tree.update(4, 10)
    result = tree.query(0, 4)

    # Assert
    assert result == 24  # 5 + 2 + 3 + 4 + 10


def test_segment_tree_query_single_element() -> None:
    """
    Test case 6: Query single element.
    """
    # Arrange
    tree = SegmentTree()
    arr = [1, 2, 3, 4, 5]
    tree.build(arr)

    # Act
    result = tree.query(2, 2)

    # Assert
    assert result == 3


def test_segment_tree_empty_initialization() -> None:
    """
    Test case 7: Empty segment tree initialization.
    """
    # Act
    tree = SegmentTree()

    # Assert
    assert tree.n == 0
    assert len(tree.tree) == 0


def test_segment_tree_large_array() -> None:
    """
    Test case 8: Build and query large array.
    """
    # Arrange
    tree = SegmentTree()
    arr = list(range(1, 101))  # 1 to 100

    # Act
    tree.build(arr)
    result = tree.query(0, 99)

    # Assert
    assert result == 5050  # Sum of 1 to 100
