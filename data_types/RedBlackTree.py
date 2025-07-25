class RedBlackNode:
    """
    A node in a Red-Black Tree.

    Attributes
    ----------
    key : int
        The key of the node.
    left : Optional[RedBlackNode]
        The left child of the node.
    right : Optional[RedBlackNode]
        The right child of the node.
    color : str
        The color of the node ('RED' or 'BLACK').
    parent : Optional[RedBlackNode]
        The parent of the node.
    """

    def __init__(self, key: int) -> None:
        self.key: int = key
        self.left: RedBlackNode | None = None
        self.right: RedBlackNode | None = None
        self.color: str = "RED"
        self.parent: RedBlackNode | None = None


class RedBlackTree:
    """
    A Red-Black Tree data structure.

    Attributes
    ----------
    root : Optional[RedBlackNode]
        The root node of the Red-Black Tree.

    Methods
    -------
    insert(key: int) -> None
        Inserts a key into the Red-Black Tree.
    _fix_insert(node: RedBlackNode) -> None
        Fixes violations of the Red-Black Tree properties after insertion.
    _rotate_left(node: RedBlackNode) -> None
        Performs a left rotation on a node.
    _rotate_right(node: RedBlackNode) -> None
        Performs a right rotation on a node.
    """

    def __init__(self) -> None:
        self.root: RedBlackNode | None = None

    def insert(self, key: int) -> None:
        """
        Inserts a key into the Red-Black Tree.

        Parameters
        ----------
        key : int
            The key to insert.
        """
        new_node = RedBlackNode(key)
        if self.root is None:
            self.root = new_node
            self.root.color = "BLACK"
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

        self._fix_insert(new_node)

    def _fix_insert(self, node: RedBlackNode) -> None:
        """
        Fixes violations of the Red-Black Tree properties after insertion.

        Parameters
        ----------
        node : RedBlackNode
            The newly inserted node.
        """
        while node.parent is not None and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._rotate_left(node.parent.parent)
            self.root.color = "BLACK"

    def _rotate_left(self, node: RedBlackNode) -> None:
        """
        Performs a left rotation on a node.

        Parameters
        ----------
        node : RedBlackNode
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

    def _rotate_right(self, node: RedBlackNode) -> None:
        """
        Performs a right rotation on a node.

        Parameters
        ----------
        node : RedBlackNode
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
