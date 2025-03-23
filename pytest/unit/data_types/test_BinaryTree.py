import pytest
from data_types.BinaryTree import BinaryTree

def test_insert_single_node() -> None:
    """
    Test inserting a single node into the binary tree.
    """
    # Test case 1: Insert a single node
    tree = BinaryTree()
    tree.insert(10)
    assert tree.root is not None
    assert tree.root.data == 10
    assert tree.root.left is None
    assert tree.root.right is None

def test_insert_multiple_nodes() -> None:
    """
    Test inserting multiple nodes into the binary tree.
    """
    # Test case 2: Insert multiple nodes
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    assert tree.root is not None
    assert tree.root.data == 10
    assert tree.root.left.data == 5
    assert tree.root.right.data == 15

def test_search_existing_node() -> None:
    """
    Test searching for an existing node in the binary tree.
    """
    # Test case 3: Search for an existing node
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    assert tree.search(10) is True
    assert tree.search(5) is True
    assert tree.search(15) is True

def test_search_non_existing_node() -> None:
    """
    Test searching for a non-existing node in the binary tree.
    """
    # Test case 4: Search for a non-existing node
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    assert tree.search(20) is False
    assert tree.search(0) is False

def test_inorder_traversal() -> None:
    """
    Test in-order traversal of the binary tree.
    """
    # Test case 5: In-order traversal
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    tree.insert(3)
    tree.insert(7)
    assert tree.inorder_traversal() == [3, 5, 7, 10, 15]

def test_preorder_traversal() -> None:
    """
    Test pre-order traversal of the binary tree.
    """
    # Test case 6: Pre-order traversal
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    tree.insert(3)
    tree.insert(7)
    assert tree.preorder_traversal() == [10, 5, 3, 7, 15]

def test_postorder_traversal() -> None:
    """
    Test post-order traversal of the binary tree.
    """
    # Test case 7: Post-order traversal
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    tree.insert(3)
    tree.insert(7)
    assert tree.postorder_traversal() == [3, 7, 5, 15, 10]

def test_empty_tree_traversals() -> None:
    """
    Test traversals on an empty binary tree.
    """
    # Test case 8: Traversals on an empty tree
    tree = BinaryTree()
    assert tree.inorder_traversal() == []
    assert tree.preorder_traversal() == []
    assert tree.postorder_traversal() == []

def test_insert_left_and_right_nodes() -> None:
    """
    Test inserting nodes to the left and right of the root.
    """
    # Test case 9: Insert left and right nodes
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)  # Left child
    tree.insert(15)  # Right child
    assert tree.root.left.data == 5
    assert tree.root.right.data == 15

def test_search_in_empty_tree() -> None:
    """
    Test searching for a value in an empty binary tree.
    """
    # Test case 10: Search in an empty tree
    tree = BinaryTree()
    assert tree.search(10) is False  # Should return False as the tree is empty

def test_traversals_with_single_node() -> None:
    """
    Test traversals on a binary tree with a single node.
    """
    # Test case 11: Traversals with a single node
    tree = BinaryTree()
    tree.insert(10)
    assert tree.inorder_traversal() == [10]
    assert tree.preorder_traversal() == [10]
    assert tree.postorder_traversal() == [10]

def test_inorder_traversal_with_left_heavy_tree() -> None:
    """
    Test in-order traversal on a left-heavy binary tree.
    """
    # Test case 12: In-order traversal with a left-heavy tree
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(3)
    tree.insert(2)
    assert tree.inorder_traversal() == [2, 3, 5, 10]  # Left-heavy tree

def test_preorder_traversal_with_left_heavy_tree() -> None:
    """
    Test pre-order traversal on a left-heavy binary tree.
    """
    # Test case 13: Pre-order traversal with a left-heavy tree
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(3)
    tree.insert(2)
    assert tree.preorder_traversal() == [10, 5, 3, 2]  # Left-heavy tree

def test_postorder_traversal_with_left_heavy_tree() -> None:
    """
    Test post-order traversal on a left-heavy binary tree.
    """
    # Test case 14: Post-order traversal with a left-heavy tree
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(3)
    tree.insert(2)
    assert tree.postorder_traversal() == [2, 3, 5, 10]  # Left-heavy tree

def test_insert_and_search_large_tree() -> None:
    """
    Test inserting and searching in a large binary tree.
    """
    # Test case 15: Insert and search in a large tree
    tree = BinaryTree()
    for i in range(1, 101):  # Insert values 1 to 100
        tree.insert(i)
    for i in range(1, 101):  # Search for values 1 to 100
        assert tree.search(i) is True
    assert tree.search(101) is False  # Value not in the tree

def test_traversals_with_large_tree() -> None:
    """
    Test traversals on a large binary tree.
    """
    # Test case 16: Traversals with a large tree
    tree = BinaryTree()
    for i in range(1, 11):  # Insert values 1 to 10
        tree.insert(i)
    assert tree.inorder_traversal() == list(range(1, 11))  # In-order should be sorted
    assert tree.preorder_traversal() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Pre-order for right-heavy tree
    assert tree.postorder_traversal() == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]  # Post-order for right-heavy tree

def test_inorder_traversal_with_right_heavy_tree() -> None:
    """
    Test in-order traversal on a right-heavy binary tree.
    """
    # Test case 17: In-order traversal with a right-heavy tree
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(15)
    tree.insert(20)
    tree.insert(25)
    assert tree.inorder_traversal() == [10, 15, 20, 25]  # Right-heavy tree

def test_preorder_traversal_with_right_heavy_tree() -> None:
    """
    Test pre-order traversal on a right-heavy binary tree.
    """
    # Test case 18: Pre-order traversal with a right-heavy tree
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(15)
    tree.insert(20)
    tree.insert(25)
    assert tree.preorder_traversal() == [10, 15, 20, 25]  # Right-heavy tree

def test_postorder_traversal_with_right_heavy_tree() -> None:
    """
    Test post-order traversal on a right-heavy binary tree.
    """
    # Test case 19: Post-order traversal with a right-heavy tree
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(15)
    tree.insert(20)
    tree.insert(25)
    assert tree.postorder_traversal() == [25, 20, 15, 10]  # Right-heavy tree

def test_insert_boundary_values() -> None:
    """
    Test inserting the smallest and largest possible values into the binary tree.
    """
    # Test case 20: Insert boundary values
    tree = BinaryTree()
    tree.insert(float('-inf'))
    tree.insert(float('inf'))
    assert tree.root is not None
    assert tree.root.data == float('-inf')  # Smallest value should be the root
    assert tree.root.right.data == float('inf')  # Largest value should be the right child
    assert tree.inorder_traversal() == [float('-inf'), float('inf')]

def test_insert_duplicate_node() -> None:
    """
    Test inserting duplicate nodes into the binary tree.
    """
    # Test case 21: Insert duplicate nodes
    tree = BinaryTree()
    tree.insert(10)
    with pytest.raises(ValueError, match="Duplicate values are not allowed in the BinaryTree"):
        tree.insert(10)  # Duplicate node