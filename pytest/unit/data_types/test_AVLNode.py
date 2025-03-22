import pytest
from data_types.AVLNode import AVLTree, AVLNode

def test_insert_single_node():
    """
    Test inserting a single node into the AVL tree.
    """
    # Test case 1: Insert a single node
    tree = AVLTree()
    tree.insert(10)
    assert tree.root is not None
    assert tree.root.key == 10
    assert tree.root.height == 1

def test_insert_multiple_nodes():
    """
    Test inserting multiple nodes and check balancing.
    """
    # Test case 2: Insert multiple nodes and trigger balancing
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)  # This should trigger a left rotation.
    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30

def test_delete_leaf_node():
    """
    Test deleting a leaf node.
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

def test_delete_node_with_one_child():
    """
    Test deleting a node with one child.
    """
    # Test case 4: Delete a node with one child
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.delete(10)
    assert tree.root.key == 20
    assert tree.root.left is None

def test_delete_node_with_two_children():
    """
    Test deleting a node with two children.
    """
    # Test case 5: Delete a node with two children
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(5)
    tree.insert(15)
    tree.delete(10)  # Root node with two children.
    assert tree.root.key == 15  # Successor replaces the root.
    assert tree.root.left.key == 5
    assert tree.root.right.key == 20

def test_search_existing_key():
    """
    Test searching for an existing key.
    """
    # Test case 6: Search for an existing key
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    node = tree.search(20)
    assert node is not None
    assert node.key == 20

def test_search_non_existing_key():
    """
    Test searching for a non-existing key.
    """
    # Test case 7: Search for a non-existing key
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    node = tree.search(30)
    assert node is None

def test_empty_tree():
    """
    Test operations on an empty tree.
    """
    # Test case 8: Perform operations on an empty tree
    tree = AVLTree()
    assert tree.root is None
    assert tree.search(10) is None
    tree.delete(10)  # Should not raise an error.

def test_balance_after_insertions():
    """
    Test that the AVL tree remains balanced after multiple insertions.
    """
    # Test case 9: Check balance after multiple insertions
    tree = AVLTree()
    for key in [10, 20, 30, 40, 50, 25]:
        tree.insert(key)
    assert tree.root.key == 30
    assert tree.root.left.key == 20
    assert tree.root.right.key == 40
    assert tree.root.left.left.key == 10
    assert tree.root.left.right.key == 25
    assert tree.root.right.right.key == 50

def test_balance_after_deletions():
    """
    Test that the AVL tree remains balanced after multiple deletions.
    """
    # Test case 10: Check balance after multiple deletions
    tree = AVLTree()
    for key in [10, 20, 30, 40, 50, 25]:
        tree.insert(key)
    tree.delete(50)
    tree.delete(40)
    assert tree.root.key == 30
    assert tree.root.left.key == 20
    assert tree.root.right.key == 25
    assert tree.root.left.left.key == 10