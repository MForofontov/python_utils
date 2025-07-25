from typing import TypeVar, Generic

# Define a generic type variable
T = TypeVar("T")


class AVLNode(Generic[T]):
    """
    A node in an AVL tree.

    Attributes
    ----------
    key : T
        The key of the node.
    left : Optional[AVLNode[T]]
        The left child of the node.
    right : Optional[AVLNode[T]]
        The right child of the node.
    height : int
        The height of the node.
    """

    def __init__(self, key: T) -> None:
        self.key: T = key
        self.left: AVLNode[T] | None = None
        self.right: AVLNode[T] | None = None
        self.height: int = 1


class AVLTree(Generic[T]):
    """
    An AVL Tree data structure.

    Attributes
    ----------
    root : Optional[AVLNode[T]]
        The root node of the AVL tree.

    Methods
    -------
    insert(key: T) -> None
        Inserts a key into the AVL tree.
    delete(key: T) -> None
        Deletes a key from the AVL tree.
    search(key: T) -> Optional[AVLNode[T]]
        Searches for a key in the AVL tree.
    """

    def __init__(self) -> None:
        self.root: AVLNode[T] | None = None

    def insert(self, key: T) -> None:
        """
        Inserts a key into the AVL tree.

        Parameters
        ----------
        key : T
            The key to insert.
        """
        self.root = self._insert(self.root, key)

    def _insert(self, node: AVLNode[T] | None, key: T) -> AVLNode[T]:
        if node is None:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Duplicate key, do not insert
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def delete(self, key: T) -> None:
        """
        Deletes a key from the AVL tree.

        Parameters
        ----------
        key : T
            The key to delete.
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node: AVLNode[T] | None, key: T) -> AVLNode[T] | None:
        if node is None:
            raise ValueError("Key not found")
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

    def search(self, key: T) -> AVLNode[T] | None:
        """
        Searches for a key in the AVL tree.

        Parameters
        ----------
        key : T
            The key to search for.

        Returns
        -------
        Optional[AVLNode[T]]
            The node containing the key, or None if not found.
        """
        return self._search(self.root, key)

    def _search(self, node: AVLNode[T] | None, key: T) -> AVLNode[T] | None:
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def _rotate_left(self, node: AVLNode[T]) -> AVLNode[T]:
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        right_child.height = 1 + max(
            self._get_height(right_child.left), self._get_height(right_child.right)
        )
        return right_child

    def _rotate_right(self, node: AVLNode[T]) -> AVLNode[T]:
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        left_child.height = 1 + max(
            self._get_height(left_child.left), self._get_height(left_child.right)
        )
        return left_child

    def _balance(self, node: AVLNode[T]) -> AVLNode[T]:
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

    def _get_height(self, node: AVLNode[T] | None) -> int:
        return 0 if node is None else node.height

    def _get_balance(self, node: AVLNode[T] | None) -> int:
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_min_value_node(self, node: AVLNode[T]) -> AVLNode[T]:
        current = node
        while current.left is not None:
            current = current.left
        return current
