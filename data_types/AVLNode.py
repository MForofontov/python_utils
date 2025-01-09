from typing import Optional

class AVLNode:
    """
    A node in an AVL tree.

    Attributes
    ----------
    key : int
        The key of the node.
    left : Optional[AVLNode]
        The left child of the node.
    right : Optional[AVLNode]
        The right child of the node.
    height : int
        The height of the node.

    Methods
    -------
    __init__(key: int) -> None
        Initializes an AVL node.
    """

    def __init__(self, key: int) -> None:
        self.key: int = key
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height: int = 1


class AVLTree:
    """
    An AVL Tree data structure.

    Attributes
    ----------
    root : Optional[AVLNode]
        The root node of the AVL tree.

    Methods
    -------
    insert(key: int) -> None
        Inserts a key into the AVL tree.
    delete(key: int) -> None
        Deletes a key from the AVL tree.
    search(key: int) -> Optional[AVLNode]
        Searches for a key in the AVL tree.
    _rotate_left(node: AVLNode) -> AVLNode
        Performs a left rotation on a node.
    _rotate_right(node: AVLNode) -> AVLNode
        Performs a right rotation on a node.
    _balance(node: AVLNode) -> AVLNode
        Balances the AVL tree.
    _get_height(node: Optional[AVLNode]) -> int
        Returns the height of a node.
    _get_balance(node: AVLNode) -> int
        Returns the balance factor of a node.
    """

    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None

    def insert(self, key: int) -> None:
        """
        Inserts a key into the AVL tree.

        Parameters
        ----------
        key : int
            The key to insert.
        """
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[AVLNode], key: int) -> AVLNode:
        if node is None:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def delete(self, key: int) -> None:
        """
        Deletes a key from the AVL tree.

        Parameters
        ----------
        key : int
            The key to delete.
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def search(self, key: int) -> Optional[AVLNode]:
        """
        Searches for a key in the AVL tree.

        Parameters
        ----------
        key : int
            The key to search for.

        Returns
        -------
        Optional[AVLNode]
            The node containing the key, or None if not found.
        """
        return self._search(self.root, key)

    def _search(self, node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        right_child.height = 1 + max(self._get_height(right_child.left), self._get_height(right_child.right))
        return right_child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        left_child.height = 1 + max(self._get_height(left_child.left), self._get_height(left_child.right))
        return left_child

    def _balance(self, node: AVLNode) -> AVLNode:
        balance = self._get_balance(node)

        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_height(self, node: Optional[AVLNode]) -> int:
        return 0 if node is None else node.height

    def _get_balance(self, node: AVLNode) -> int:
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_min_value_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left is not None:
            current = current.left
        return current
