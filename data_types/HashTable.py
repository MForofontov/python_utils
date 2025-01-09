from typing import List, Tuple, Any

class HashTable:
    """
    A simple Hash Table data structure.

    Attributes
    ----------
    size : int
        The number of buckets in the hash table.
    table : List[List[Tuple[Any, Any]]]
        The list of buckets where each bucket stores key-value pairs as tuples.

    Methods
    -------
    insert(key, value)
        Inserts a key-value pair into the hash table.
    get(key)
        Retrieves the value associated with a key.
    remove(key)
        Removes a key-value pair from the hash table.
    contains(key)
        Checks if the hash table contains a key.
    """

    def __init__(self, size: int = 10) -> None:
        """
        Initializes the hash table with a given size.

        Parameters
        ----------
        size : int
            The number of buckets in the hash table. Default is 10.
        """
        self.size = size
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.size)]

    def _hash(self, key: Any) -> int:
        """
        Hash function to compute the index for a given key.

        Parameters
        ----------
        key : Any
            The key to hash.

        Returns
        -------
        int
            The index for the key in the table.
        """
        return hash(key) % self.size

    def insert(self, key: Any, value: Any) -> None:
        """
        Inserts a key-value pair into the hash table.

        Parameters
        ----------
        key : Any
            The key to insert.
        value : Any
            The value associated with the key.
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def get(self, key: Any) -> Any:
        """
        Retrieves the value associated with a key.

        Parameters
        ----------
        key : Any
            The key to look up.

        Returns
        -------
        Any
            The value associated with the key.

        Raises
        ------
        KeyError
            If the key is not found in the hash table.
        """
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found in the hash table")

    def remove(self, key: Any) -> None:
        """
        Removes a key-value pair from the hash table.

        Parameters
        ----------
        key : Any
            The key to remove.

        Raises
        ------
        KeyError
            If the key is not found in the hash table.
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return
        raise KeyError(f"Key {key} not found in the hash table")

    def contains(self, key: Any) -> bool:
        """
        Checks if the hash table contains a key.

        Parameters
        ----------
        key : Any
            The key to check.

        Returns
        -------
        bool
            True if the key exists, False otherwise.
        """
        index = self._hash(key)
        for k, _ in self.table[index]:
            if k == key:
                return True
        return False
