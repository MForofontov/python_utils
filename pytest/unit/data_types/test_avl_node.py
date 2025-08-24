import pytest
from data_types.avl_node import AVLTree


def test_insert_single_node() -> None:
    """
    Test case 1: Test inserting a single node into the AVL tree.
    """
    tree = AVLTree[int]()  # Specify the type as int
    tree.insert(10)
    assert tree.root is not None
    assert tree.root.key == 10
    assert tree.root.height == 1


def test_insert_multiple_nodes_balanced() -> None:
    """
    Test case 2: Test inserting multiple nodes and ensuring the tree remains balanced.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)  # This should trigger a left rotation
    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30


def test_delete_leaf_node() -> None:
    """
    Test case 3: Test deleting a leaf node from the AVL tree.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.delete(30)
    assert tree.root.right is not None
    assert tree.root.right.key == 20
    assert tree.root.right.right is None


def test_delete_node_with_one_child() -> None:
    """
    Test case 4: Test deleting a node with one child.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(15)
    tree.delete(20)
    assert tree.root.right is not None
    assert tree.root.right.key == 15


def test_delete_node_with_two_children() -> None:
    """
    Test case 5: Test deleting a node with two children.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(15)
    tree.insert(25)
    tree.delete(20)
    assert tree.root.right is not None
    assert tree.root.right.key == 25
    assert tree.root.right.left.key == 15


def test_search_existing_key() -> None:
    """
    Test case 6: Test searching for an existing key in the AVL tree.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    node = tree.search(20)
    assert node is not None
    assert node.key == 20


def test_search_non_existing_key() -> None:
    """
    Test case 7: Test searching for a non-existing key in the AVL tree.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    node = tree.search(40)
    assert node is None


def test_balance_after_insertions() -> None:
    """
    Test case 8: Test that the AVL tree remains balanced after multiple insertions.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.insert(40)
    tree.insert(50)
    # Root should be 20 after balancing
    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 40


def test_height_update_after_operations() -> None:
    """
    Test case 9: Test that the height of nodes is updated correctly after operations.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    assert tree.root.height == 2
    tree.delete(30)
    # Height remains 2 after rebalancing
    assert tree.root.height == 2


def test_delete_non_existing_key() -> None:
    """
    Test case 10: Test deleting a non-existing key from the AVL tree.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    with pytest.raises(ValueError):
        tree.delete(30)
    assert tree.root.key == 10
    assert tree.root.right.key == 20


def test_insert_duplicate_key() -> None:
    """
    Test case 11: Test inserting a duplicate key into the AVL tree.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(10)  # Duplicate key
    assert tree.root is not None
    assert tree.root.key == 10
    assert tree.root.left is None
    assert tree.root.right is None  # No duplicate node should be added


def test_delete_root_node() -> None:
    """
    Test case 12: Test deleting the root node of the AVL tree.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(5)
    tree.delete(10)
    assert tree.root is not None
    assert tree.root.key in [5, 20]


def test_large_tree_balance() -> None:
    """
    Test case 13: Test the balance of a large AVL tree after multiple insertions.
    """
    tree = AVLTree[int]()
    for i in range(1, 101):
        tree.insert(i)
    assert tree.root is not None
    assert abs(tree._get_balance(tree.root)) <= 1


def test_delete_all_nodes() -> None:
    """
    Test case 14: Test deleting all nodes from the AVL tree.
    """
    tree = AVLTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.delete(10)
    tree.delete(20)
    tree.delete(30)
    assert tree.root is None


def test_search_in_empty_tree() -> None:
    """
    Test case 15: Test searching for a key in an empty AVL tree.
    """
    tree = AVLTree[int]()
    node = tree.search(10)
    assert node is None


def test_height_of_empty_tree() -> None:
    """
    Test case 16: Test the height of an empty AVL tree.
    """
    tree = AVLTree[int]()
    assert tree._get_height(tree.root) == 0


def test_balance_of_empty_tree() -> None:
    """
    Test case 17: Test the balance factor of an empty AVL tree.
    """
    tree = AVLTree[int]()
    assert tree._get_balance(tree.root) == 0
