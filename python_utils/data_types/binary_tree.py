from typing import TypeVar, Generic

# Define a generic type variable
T = TypeVar("T")


class BinaryTreeNode(Generic[T]):
    """
    A node in the binary tree.

    Attributes
    ----------
    data : T
        The data stored in the node.
    left : Optional[BinaryTreeNode[T]]
        The left child of the node.
    right : Optional[BinaryTreeNode[T]]
        The right child of the node.
    """

    def __init__(self, data: T) -> None:
        self.data: T = data
        self.left: BinaryTreeNode[T] | None = None
        self.right: BinaryTreeNode[T] | None = None


class BinaryTree(Generic[T]):
    """
    A binary tree data structure.

    Attributes
    ----------
    root : Optional[BinaryTreeNode[T]]
        The root node of the binary tree.

    Methods
    -------
    insert(data: T) -> None
        Inserts data into the binary tree.
    search(data: T) -> bool
        Searches for data in the binary tree.
    inorder_traversal() -> List[T]
        Performs an in-order traversal of the tree.
    preorder_traversal() -> List[T]
        Performs a pre-order traversal of the tree.
    postorder_traversal() -> List[T]
        Performs a post-order traversal of the tree.

    Raises
    ------
    ValueError
        If duplicate values are inserted into the binary tree.
    """

    def __init__(self) -> None:
        self.root: BinaryTreeNode[T] | None = None

    def insert(self, data: T) -> None:
        """
        Inserts data into the binary tree.

        Parameters
        ----------
        data : T
            The data to insert into the binary tree.
        """
        if self.root is None:
            self.root = BinaryTreeNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node: BinaryTreeNode[T], data: T) -> None:
        """
        A helper method to insert data recursively.

        Parameters
        ----------
        node : BinaryTreeNode[T]
            The current node to check for insertion.
        data : T
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
            raise ValueError(
                "Duplicate values are not allowed in the BinaryTree")

    def search(self, data: T) -> bool:
        """
        Searches for data in the binary tree.

        Parameters
        ----------
        data : T
            The data to search for.

        Returns
        -------
        bool
            True if the data is found, False otherwise.
        """
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node: BinaryTreeNode[T] | None, data: T) -> bool:
        """
        A helper method to search for data recursively.

        Parameters
        ----------
        node : Optional[BinaryTreeNode[T]]
            The current node to check for data.
        data : T
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

    def inorder_traversal(self) -> list[T]:
        """
        Performs an in-order traversal of the tree.

        Returns
        -------
        List[T]
            A list of data in in-order.
        """
        return self._inorder_traversal_recursive(self.root)

    def _inorder_traversal_recursive(self, node: BinaryTreeNode[T] | None) -> list[T]:
        """
        A helper method to perform an in-order traversal recursively.

        Parameters
        ----------
        node : Optional[BinaryTreeNode[T]]
            The current node to traverse.

        Returns
        -------
        List[T]
            A list of data in in-order.
        """
        if node is None:
            return []
        return (
            self._inorder_traversal_recursive(node.left)
            + [node.data]
            + self._inorder_traversal_recursive(node.right)
        )

    def preorder_traversal(self) -> list[T]:
        """
        Performs a pre-order traversal of the tree.

        Returns
        -------
        List[T]
            A list of data in pre-order.
        """
        return self._preorder_traversal_recursive(self.root)

    def _preorder_traversal_recursive(self, node: BinaryTreeNode[T] | None) -> list[T]:
        """
        A helper method to perform a pre-order traversal recursively.

        Parameters
        ----------
        node : Optional[BinaryTreeNode[T]]
            The current node to traverse.

        Returns
        -------
        List[T]
            A list of data in pre-order.
        """
        if node is None:
            return []
        return (
            [node.data]
            + self._preorder_traversal_recursive(node.left)
            + self._preorder_traversal_recursive(node.right)
        )

    def postorder_traversal(self) -> list[T]:
        """
        Performs a post-order traversal of the tree.

        Returns
        -------
        List[T]
            A list of data in post-order.
        """
        return self._postorder_traversal_recursive(self.root)

    def _postorder_traversal_recursive(self, node: BinaryTreeNode[T] | None) -> list[T]:
        """
        A helper method to perform a post-order traversal recursively.

        Parameters
        ----------
        node : Optional[BinaryTreeNode[T]]
            The current node to traverse.

        Returns
        -------
        List[T]
            A list of data in post-order.
        """
        if node is None:
            return []
        return (
            self._postorder_traversal_recursive(node.left)
            + self._postorder_traversal_recursive(node.right)
            + [node.data]
        )
