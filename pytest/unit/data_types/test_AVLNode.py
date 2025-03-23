import pytest
from data_types.AVLNode import AVLTree, AVLNode

def test_insert_single_node() -> None:
    """
    Test inserting a single node into the AVL tree.
    """
    # Test case 1: Insert a single node
    tree = AVLTree()
    tree.insert(10)
    assert tree.root is not None
    assert tree.root.key == 10
    assert tree.root.height == 1

def test_insert_multiple_nodes_balanced() -> None:
    """
    Test inserting multiple nodes and ensuring the tree remains balanced.
    """
    # Test case 2: Insert multiple nodes
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)  # This should trigger a left rotation
    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30

def test_delete_leaf_node() -> None:
    """
    Test deleting a leaf node from the AVL tree.
    """
    # Test case 3: Delete a leaf node
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.delete(30)
    assert tree.root.right is not None
    assert tree.root.right.key == 20
    assert tree.root.right.right is None

def test_delete_node_with_one_child() -> None:
    """
    Test deleting a node with one child.
    """
    # Test case 4: Delete a node with one child
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(15)
    tree.delete(20)
    assert tree.root.right is not None
    assert tree.root.right.key == 15

def test_delete_node_with_two_children() -> None:
    """
    Test deleting a node with two children.
    """
    # Test case 5: Delete a node with two children
    tree = AVLTree()
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
    Test searching for an existing key in the AVL tree.
    """
    # Test case 6: Search for an existing key
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    node = tree.search(20)
    assert node is not None
    assert node.key == 20

def test_search_non_existing_key() -> None:
    """
    Test searching for a non-existing key in the AVL tree.
    """
    # Test case 7: Search for a non-existing key
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    node = tree.search(40)
    assert node is None

def test_balance_after_insertions() -> None:
    """
    Test that the AVL tree remains balanced after multiple insertions.
    """
    # Test case 8: Ensure balance after insertions
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.insert(40)
    tree.insert(50)
    assert tree.root.key == 30
    assert tree.root.left.key == 20
    assert tree.root.right.key == 40

def test_height_update_after_operations() -> None:
    """
    Test that the height of nodes is updated correctly after operations.
    """
    # Test case 9: Verify height updates
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    assert tree.root.height == 2
    tree.delete(30)
    assert tree.root.height == 1

def test_delete_non_existing_key() -> None:
    """
    Test deleting a non-existing key from the AVL tree.
    """
    # Test case 10: Delete a non-existing key
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    with pytest.raises(ValueError):
        tree.delete(30)  # Should not raise an error
    assert tree.root.key == 10
    assert tree.root.right.key == 20

def test_insert_duplicate_key() -> None:
    """
    Test inserting a duplicate key into the AVL tree.
    """
    # Test case 11: Insert a duplicate key
    tree = AVLTree()
    tree.insert(10)
    tree.insert(10)  # Duplicate key
    assert tree.root is not None
    assert tree.root.key == 10
    assert tree.root.left is None
    assert tree.root.right is None  # No duplicate node should be added

def test_delete_root_node() -> None:
    """
    Test deleting the root node of the AVL tree.
    """
    # Test case 12: Delete the root node
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(5)
    tree.delete(10)  # Delete the root
    assert tree.root is not None
    assert tree.root.key in [5, 20]  # Either 5 or 20 becomes the new root

def test_large_tree_balance() -> None:
    """
    Test the balance of a large AVL tree after multiple insertions.
    """
    # Test case 13: Large tree balance
    tree = AVLTree()
    for i in range(1, 101):  # Insert 100 nodes
        tree.insert(i)
    assert tree.root is not None
    assert abs(tree._get_balance(tree.root)) <= 1  # Root should be balanced

def test_delete_all_nodes() -> None:
    """
    Test deleting all nodes from the AVL tree.
    """
    # Test case 14: Delete all nodes
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.delete(10)
    tree.delete(20)
    tree.delete(30)
    assert tree.root is None  # Tree should be empty

def test_search_in_empty_tree() -> None:
    """
    Test searching for a key in an empty AVL tree.
    """
    # Test case 15: Search in an empty tree
    tree = AVLTree()
    node = tree.search(10)
    assert node is None  # Should return None as the tree is empty

def test_height_of_empty_tree() -> None:
    """
    Test the height of an empty AVL tree.
    """
    # Test case 16: Height of an empty tree
    tree = AVLTree()
    assert tree._get_height(tree.root) == 0  # Height of an empty tree should be 0

def test_balance_of_empty_tree() -> None:
    """
    Test the balance factor of an empty AVL tree.
    """
    # Test case 17: Balance of an empty tree
    tree = AVLTree()
    assert tree._get_balance(tree.root) == 0  # Balance factor of an empty tree should be 0