from data_types.binary_tree import BinaryTree

import pytest


def test_insert_single_node() -> None:
    """
    Test case 1: Test inserting a single node into the binary tree.
    """
    tree = BinaryTree[int]()  # Specify the type as int
    tree.insert(10)
    assert tree.root is not None
    assert tree.root.data == 10
    assert tree.root.left is None
    assert tree.root.right is None


def test_insert_multiple_nodes() -> None:
    """
    Test case 2: Test inserting multiple nodes into the binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    assert tree.root is not None
    assert tree.root.data == 10
    assert tree.root.left.data == 5
    assert tree.root.right.data == 15


def test_search_existing_node() -> None:
    """
    Test case 3: Test searching for an existing node in the binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    assert tree.search(10) is True
    assert tree.search(5) is True
    assert tree.search(15) is True


def test_search_non_existing_node() -> None:
    """
    Test case 4: Test searching for a non-existing node in the binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    assert tree.search(20) is False
    assert tree.search(0) is False


def test_inorder_traversal() -> None:
    """
    Test case 5: Test in-order traversal of the binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    tree.insert(3)
    tree.insert(7)
    assert tree.inorder_traversal() == [3, 5, 7, 10, 15]


def test_preorder_traversal() -> None:
    """
    Test case 6: Test pre-order traversal of the binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    tree.insert(3)
    tree.insert(7)
    assert tree.preorder_traversal() == [10, 5, 3, 7, 15]


def test_postorder_traversal() -> None:
    """
    Test case 7: Test post-order traversal of the binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    tree.insert(3)
    tree.insert(7)
    assert tree.postorder_traversal() == [3, 7, 5, 15, 10]


def test_empty_tree_traversals() -> None:
    """
    Test case 8: Test traversals on an empty binary tree.
    """
    tree = BinaryTree[int]()
    assert tree.inorder_traversal() == []
    assert tree.preorder_traversal() == []
    assert tree.postorder_traversal() == []


def test_insert_left_and_right_nodes() -> None:
    """
    Test case 9: Test inserting nodes to the left and right of the root.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)  # Left child
    tree.insert(15)  # Right child
    assert tree.root.left.data == 5
    assert tree.root.right.data == 15


def test_search_in_empty_tree() -> None:
    """
    Test case 10: Test searching for a value in an empty binary tree.
    """
    tree = BinaryTree[int]()
    assert tree.search(10) is False  # Should return False as the tree is empty


def test_traversals_with_single_node() -> None:
    """
    Test case 11: Test traversals on a binary tree with a single node.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    assert tree.inorder_traversal() == [10]
    assert tree.preorder_traversal() == [10]
    assert tree.postorder_traversal() == [10]


def test_inorder_traversal_with_left_heavy_tree() -> None:
    """
    Test case 12: Test in-order traversal on a left-heavy binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(3)
    tree.insert(2)
    assert tree.inorder_traversal() == [2, 3, 5, 10]  # Left-heavy tree


def test_preorder_traversal_with_left_heavy_tree() -> None:
    """
    Test case 13: Test pre-order traversal on a left-heavy binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(3)
    tree.insert(2)
    assert tree.preorder_traversal() == [10, 5, 3, 2]  # Left-heavy tree


def test_postorder_traversal_with_left_heavy_tree() -> None:
    """
    Test case 14: Test post-order traversal on a left-heavy binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(5)
    tree.insert(3)
    tree.insert(2)
    assert tree.postorder_traversal() == [2, 3, 5, 10]  # Left-heavy tree


def test_insert_and_search_large_tree() -> None:
    """
    Test case 15: Test inserting and searching in a large binary tree.
    """
    tree = BinaryTree[int]()
    for i in range(1, 101):  # Insert values 1 to 100
        tree.insert(i)
    for i in range(1, 101):  # Search for values 1 to 100
        assert tree.search(i) is True
    assert tree.search(101) is False  # Value not in the tree


def test_traversals_with_large_tree() -> None:
    """
    Test case 16: Test traversals on a large binary tree.
    """
    tree = BinaryTree[int]()
    for i in range(1, 11):  # Insert values 1 to 10
        tree.insert(i)
    assert tree.inorder_traversal() == list(range(1, 11))  # In-order should be sorted
    assert tree.preorder_traversal() == [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
    ]  # Pre-order for right-heavy tree
    assert tree.postorder_traversal() == [
        10,
        9,
        8,
        7,
        6,
        5,
        4,
        3,
        2,
        1,
    ]  # Post-order for right-heavy tree


def test_inorder_traversal_with_right_heavy_tree() -> None:
    """
    Test case 17: Test in-order traversal on a right-heavy binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(15)
    tree.insert(20)
    tree.insert(25)
    assert tree.inorder_traversal() == [10, 15, 20, 25]  # Right-heavy tree


def test_preorder_traversal_with_right_heavy_tree() -> None:
    """
    Test case 18: Test pre-order traversal on a right-heavy binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(15)
    tree.insert(20)
    tree.insert(25)
    assert tree.preorder_traversal() == [10, 15, 20, 25]  # Right-heavy tree


def test_postorder_traversal_with_right_heavy_tree() -> None:
    """
    Test case 19: Test post-order traversal on a right-heavy binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(15)
    tree.insert(20)
    tree.insert(25)
    assert tree.postorder_traversal() == [25, 20, 15, 10]  # Right-heavy tree


def test_insert_boundary_values() -> None:
    """
    Test case 20: Test inserting the smallest and largest possible values into the binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(float("-inf"))
    tree.insert(float("inf"))
    assert tree.root is not None
    assert tree.root.data == float("-inf")  # Smallest value should be the root
    assert tree.root.right.data == float(
        "inf"
    )  # Largest value should be the right child
    assert tree.inorder_traversal() == [float("-inf"), float("inf")]


def test_insert_duplicate_node() -> None:
    """
    Test case 21: Test inserting duplicate nodes into the binary tree.
    """
    tree = BinaryTree[int]()
    tree.insert(10)
    with pytest.raises(
        ValueError, match="Duplicate values are not allowed in the BinaryTree"
    ):
        tree.insert(10)  # Duplicate node
