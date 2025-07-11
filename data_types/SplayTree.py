
class SplayNode:
    """
    A node in a Splay Tree.

    Attributes
    ----------
    key : int
        The key of the node.
    left : Optional[SplayNode]
        The left child of the node.
    right : Optional[SplayNode]
        The right child of the node.
    parent : Optional[SplayNode]
        The parent of the node.
    """

    def __init__(self, key: int) -> None:
        self.key: int = key
        self.left: SplayNode | None = None
        self.right: SplayNode | None = None
        self.parent: SplayNode | None = None


class SplayTree:
    """
    A Splay Tree data structure.

    Attributes
    ----------
    root : Optional[SplayNode]
        The root node of the Splay Tree.

    Methods
    -------
    insert(key: int) -> None
        Inserts a key into the Splay Tree.
    search(key: int) -> Optional[SplayNode]
        Searches for a key in the Splay Tree.
    _rotate_left(node: SplayNode) -> None
        Performs a left rotation on a node.
    _rotate_right(node: SplayNode) -> None
        Performs a right rotation on a node.
    _splay(node: SplayNode) -> None
        Splays the node to the root.
    """

    def __init__(self) -> None:
        self.root: SplayNode | None = None

    def insert(self, key: int) -> None:
        """
        Inserts a key into the Splay Tree.

        Parameters
        ----------
        key : int
            The key to insert.
        """
        new_node = SplayNode(key)
        if self.root is None:
            self.root = new_node
            return
        node = self.root
        while node is not None:
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def search(self, key: int) -> SplayNode | None:
        """
        Searches for a key in the Splay Tree.

        Parameters
        ----------
        key : int
            The key to search for.

        Returns
        -------
        Optional[SplayNode]
            The node containing the key, or None if not found.
        """
        node = self.root
        while node is not None:
            if key == node.key:
                self._splay(node)
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _rotate_left(self, node: SplayNode) -> None:
        """
        Performs a left rotation on a node.

        Parameters
        ----------
        node : SplayNode
            The node to rotate.
        """
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def _rotate_right(self, node: SplayNode) -> None:
        """
        Performs a right rotation on a node.

        Parameters
        ----------
        node : SplayNode
            The node to rotate.
        """
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def _splay(self, node: SplayNode) -> None:
        """
        Splays the node to the root.

        Parameters
        ----------
        node : SplayNode
            The node to splay.
        """
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left and node.parent == node.parent.parent.left:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.right:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.left:
                self._rotate_left(node.parent)
                self._rotate_right(node.parent)
            else:
                self._rotate_right(node.parent)
                self._rotate_left(node.parent)

       