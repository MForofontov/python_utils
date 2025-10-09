"""Unit tests for SplayTree class."""
from data_types.splay_tree import SplayNode, SplayTree


def test_splay_tree_initialization() -> None:
    """
    Test case 1: SplayTree initialization.
    """
    # Act
    tree = SplayTree()

    # Assert
    assert tree.root is None


def test_splay_tree_insert_single_node() -> None:
    """
    Test case 2: Insert single node into empty tree.
    """
    # Arrange
    tree = SplayTree()

    # Act
    tree.insert(10)

    # Assert
    assert tree.root is not None
    assert tree.root.key == 10
    assert tree.root.left is None
    assert tree.root.right is None


def test_splay_tree_insert_multiple_nodes() -> None:
    """
    Test case 3: Insert multiple nodes.
    """
    # Arrange
    tree = SplayTree()

    # Act
    values = [10, 20, 5, 15, 25]
    for val in values:
        tree.insert(val)

    # Assert
    assert tree.root is not None
    assert tree.root.key == 25  # Last inserted should be root


def test_splay_tree_search_existing() -> None:
    """
    Test case 4: Search for existing element.
    """
    # Arrange
    tree = SplayTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(5)

    # Act
    result = tree.search(10)

    # Assert
    assert result is not None
    assert result.key == 10
    assert tree.root is not None
    assert tree.root.key == 10  # Searched element becomes root


def test_splay_tree_search_nonexistent() -> None:
    """
    Test case 5: Search for non-existent element.
    """
    # Arrange
    tree = SplayTree()
    tree.insert(10)
    tree.insert(20)

    # Act
    result = tree.search(15)

    # Assert
    assert result is None


def test_splay_tree_search_brings_to_root() -> None:
    """
    Test case 6: Search operation brings element to root.
    """
    # Arrange
    tree = SplayTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(5)
    tree.insert(15)

    # Act
    tree.search(5)

    # Assert
    assert tree.root is not None
    assert tree.root.key == 5


def test_splay_node_initialization() -> None:
    """
    Test case 7: SplayNode initialization.
    """
    # Act
    node = SplayNode(42)

    # Assert
    assert node.key == 42
    assert node.left is None
    assert node.right is None
    assert node.parent is None


def test_splay_tree_insert_ascending_order() -> None:
    """
    Test case 8: Insert nodes in ascending order.
    """
    # Arrange
    tree = SplayTree()

    # Act
    for i in range(1, 6):
        tree.insert(i)

    # Assert
    assert tree.root is not None
    assert tree.root.key == 5  # Last inserted
