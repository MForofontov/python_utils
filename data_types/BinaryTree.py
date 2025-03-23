from typing import Any, Optional

class BinaryTreeNode:
    """
    A node in the binary tree.

    Attributes
    ----------
    data : Any
        The data stored in the node.
    left : Optional[BinaryTreeNode]
        The left child of the node.
    right : Optional[BinaryTreeNode]
        The right child of the node.
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.left: Optional[BinaryTreeNode] = None
        self.right: Optional[BinaryTreeNode] = None


class BinaryTree:
    """
    A binary tree data structure.

    Attributes
    ----------
    root : Optional[BinaryTreeNode]
        The root node of the binary tree.

    Methods
    -------
    insert(data: Any) -> None
        Inserts data into the binary tree.
    search(data: Any) -> bool
        Searches for data in the binary tree.
    inorder_traversal() -> list
        Performs an in-order traversal of the tree.
    preorder_traversal() -> list
        Performs a pre-order traversal of the tree.
    postorder_traversal() -> list
        Performs a post-order traversal of the tree.
    
    Raises
    ------
    ValueError
        If duplicate values are inserted into the binary tree
    """

    def __init__(self) -> None:
        self.root: Optional[BinaryTreeNode] = None

    def insert(self, data: Any) -> None:
        """
        Inserts data into the binary tree.

        Parameters
        ----------
        data : Any
            The data to insert into the binary tree.
        """
        if self.root is None:
            self.root = BinaryTreeNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node: BinaryTreeNode, data: Any) -> None:
        """
        A helper method to insert data recursively.

        Parameters
        ----------
        node : BinaryTreeNode
            The current node to check for insertion.
        data : Any
            The data to insert.
        """
        if data < node.data:
            if node.left is None:
                node.left = BinaryTreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = BinaryTreeNode(data)
            else:
                self._insert_recursive(node.right, data)
        elif data == node.data:
            raise ValueError("Duplicate values are not allowed in the BinaryTree")

    def search(self, data: Any) -> bool:
        """
        Searches for data in the binary tree.

        Parameters
        ----------
        data : Any
            The data to search for.

        Returns
        -------
        bool
            True if the data is found, False otherwise.
        """
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node: Optional[BinaryTreeNode], data: Any) -> bool:
        """
        A helper method to search for data recursively.

        Parameters
        ----------
        node : Optional[BinaryTreeNode]
            The current node to check for data.
        data : Any
            The data to search for.

        Returns
        -------
        bool
            True if the data is found, False otherwise.
        """
        if node is None:
            return False
        if node.data == data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    def inorder_traversal(self) -> list:
        """
        Performs an in-order traversal of the tree.

        Returns
        -------
        list
            A list of data in in-order.
        """
        return self._inorder_traversal_recursive(self.root)

    def _inorder_traversal_recursive(self, node: Optional[BinaryTreeNode]) -> list:
        """
        A helper method to perform an in-order traversal recursively.

        Parameters
        ----------
        node : Optional[BinaryTreeNode]
            The current node to traverse.

        Returns
        -------
        list
            A list of data in in-order.
        """
        if node is None:
            return []
        return (self._inorder_traversal_recursive(node.left) +
                [node.data] +
                self._inorder_traversal_recursive(node.right))

    def preorder_traversal(self) -> list:
        """
        Performs a pre-order traversal of the tree.

        Returns
        -------
        list
            A list of data in pre-order.
        """
        return self._preorder_traversal_recursive(self.root)

    def _preorder_traversal_recursive(self, node: Optional[BinaryTreeNode]) -> list:
        """
        A helper method to perform a pre-order traversal recursively.

        Parameters
        ----------
        node : Optional[BinaryTreeNode]
            The current node to traverse.

        Returns
        -------
        list
            A list of data in pre-order.
        """
        if node is None:
            return []
        return [node.data] + self._preorder_traversal_recursive(node.left) + self._preorder_traversal_recursive(node.right)

    def postorder_traversal(self) -> list:
        """
        Performs a post-order traversal of the tree.

        Returns
        -------
        list
            A list of data in post-order.
        """
        return self._postorder_traversal_recursive(self.root)

    def _postorder_traversal_recursive(self, node: Optional[BinaryTreeNode]) -> list:
        """
        A helper method to perform a post-order traversal recursively.

        Parameters
        ----------
        node : Optional[BinaryTreeNode]
            The current node to traverse.

        Returns
        -------
        list
            A list of data in post-order.
        """
        if node is None:
            return []
        return (self._postorder_traversal_recursive(node.left) +
                self._postorder_traversal_recursive(node.right) +
                [node.data])
