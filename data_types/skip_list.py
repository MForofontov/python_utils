import random


class SkipNode:
    """
    A node in a Skip List.

    Attributes
    ----------
    key : int
        The key of the node.
    forward : List[Optional[SkipNode]]
        A list of forward pointers to other nodes in the Skip List at different levels.
    """

    def __init__(self, key: int, level: int) -> None:
        self.key: int = key
        self.forward: list[SkipNode | None] = [None] * (level + 1)


class SkipList:
    """
    A Skip List data structure.

    Attributes
    ----------
    max_level : int
        The maximum level of the Skip List.
    level : int
        The current level of the Skip List.
    header : SkipNode
        The header node of the Skip List.

    Methods
    -------
    insert(key: int) -> None
        Inserts a key into the Skip List.
    search(key: int) -> Optional[SkipNode]
        Searches for a key in the Skip List.
    delete(key: int) -> None
        Deletes a key from the Skip List.
    """

    def __init__(self, max_level: int) -> None:
        self.max_level = max_level
        self.level = 0
        self.header = SkipNode(-1, self.max_level)

    def insert(self, key: int) -> None:
        """
        Inserts a key into the Skip List.

        Parameters
        ----------
        key : int
            The key to insert.
        """
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current is None or current.key != key:
            level = self.random_level()
            if level > self.level:
                for i in range(self.level + 1, level + 1):
                    update[i] = self.header
                self.level = level
            new_node = SkipNode(key, level)
            for i in range(level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def search(self, key: int) -> SkipNode | None:
        """
        Searches for a key in the Skip List.

        Parameters
        ----------
        key : int
            The key to search for.

        Returns
        -------
        Optional[SkipNode]
            The node containing the key, or None if not found.
        """
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current is not None and current.key == key:
            return current
        return None

    def delete(self, key: int) -> None:
        """
        Deletes a key from the Skip List.

        Parameters
        ----------
        key : int
            The key to delete.
        """
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current is not None and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

    def random_level(self) -> int:
        """
        Generates a random level for a node.

        Returns
        -------
        int
            A random level for the node.
        """
        level = 0
        while level < self.max_level and random.random() < 0.5:
            level += 1
        return level
