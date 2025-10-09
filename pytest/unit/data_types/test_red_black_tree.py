"""Unit tests for RedBlackTree class."""
from data_types.red_black_tree import RedBlackNode, RedBlackTree


def test_red_black_tree_insert_single_node() -> None:
    """
    Test case 1: Insert single node into empty tree.
    """
    # Arrange
    tree = RedBlackTree()

    # Act
    tree.insert(10)

    # Assert
    assert tree.root is not None
    assert tree.root.key == 10
    assert tree.root.color == "BLACK"
    assert tree.root.left is None
    assert tree.root.right is None


def test_red_black_tree_insert_multiple_nodes() -> None:
    """
    Test case 2: Insert multiple nodes and verify structure.
    """
    # Arrange
    tree = RedBlackTree()

    # Act
    values = [10, 20, 5, 15, 25]
    for val in values:
        tree.insert(val)

    # Assert
    assert tree.root is not None
    assert tree.root.key in values
    assert tree.root.color == "BLACK"


def test_red_black_tree_root_always_black() -> None:
    """
    Test case 3: Root node is always black after insertions.
    """
    # Arrange
    tree = RedBlackTree()

    # Act
    for i in range(1, 11):
        tree.insert(i)

    # Assert
    assert tree.root is not None
    assert tree.root.color == "BLACK"


def test_red_black_tree_insert_ascending_order() -> None:
    """
    Test case 4: Insert nodes in ascending order.
    """
    # Arrange
    tree = RedBlackTree()

    # Act
    for i in range(1, 6):
        tree.insert(i)

    # Assert
    assert tree.root is not None
    assert tree.root.color == "BLACK"


def test_red_black_tree_insert_descending_order() -> None:
    """
    Test case 5: Insert nodes in descending order.
    """
    # Arrange
    tree = RedBlackTree()

    # Act
    for i in range(5, 0, -1):
        tree.insert(i)

    # Assert
    assert tree.root is not None
    assert tree.root.color == "BLACK"


def test_red_black_tree_insert_duplicates() -> None:
    """
    Test case 6: Insert duplicate values.
    """
    # Arrange
    tree = RedBlackTree()

    # Act
    tree.insert(10)
    tree.insert(10)
    tree.insert(10)

    # Assert
    assert tree.root is not None
    assert tree.root.key == 10


def test_red_black_node_initialization() -> None:
    """
    Test case 7: RedBlackNode initialization.
    """
    # Act
    node = RedBlackNode(42)

    # Assert
    assert node.key == 42
    assert node.color == "RED"
    assert node.left is None
    assert node.right is None
    assert node.parent is None


def test_red_black_tree_empty_initialization() -> None:
    """
    Test case 8: Empty tree initialization.
    """
    # Act
    tree = RedBlackTree()

    # Assert
    assert tree.root is None
