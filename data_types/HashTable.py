from typing import List, Tuple, TypeVar, Generic

# Define generic type variables for keys and values
K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type

class HashTable(Generic[K, V]):
    """
    A simple Hash Table data structure.

    Attributes
    ----------
    size : int
        The number of buckets in the hash table.
    table : List[List[Tuple[K, V]]]
        The list of buckets where each bucket stores key-value pairs as tuples.

    Methods
    -------
    insert(key: K, value: V) -> None
        Inserts a key-value pair into the hash table.
    get(key: K) -> V
        Retrieves the value associated with a key.
    remove(key: K) -> None
        Removes a key-value pair from the hash table.
    contains(key: K) -> bool
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
        self.table: List[List[Tuple[K, V]]] = [[] for _ in range(self.size)]

    def _hash(self, key: K) -> int:
        """
        Hash function to compute the index for a given key.

        Parameters
        ----------
        key : K
            The key to hash.

        Returns
        -------
        int
            The index for the key in the table.
        """
        return hash(key) % self.size

    def insert(self, key: K, value: V) -> None:
        """
        Inserts a key-value pair into the hash table.

        Parameters
        ----------
        key : K
            The key to insert.
        value : V
            The value associated with the key.
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def get(self, key: K) -> V:
        """
        Retrieves the value associated with a key.

        Parameters
        ----------
        key : K
            The key to look up.

        Returns
        -------
        V
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

    def remove(self, key: K) -> None:
        """
        Removes a key-value pair from the hash table.

        Parameters
        ----------
        key : K
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

    def contains(self, key: K) -> bool:
        """
        Checks if the hash table contains a key.

        Parameters
        ----------
        key : K
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