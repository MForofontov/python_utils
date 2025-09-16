from collections.abc import Iterator
from typing import Generic, TypeVar

# Define a generic type variable
T = TypeVar("T")


class Node(Generic[T]):
    """
    A Node in a Linked List.

    Attributes
    ----------
    data : T
        The data stored in the node.
    next : Node[T | None]
        The next node in the linked list, or None if it is the last node.
    """

    def __init__(self, data: T) -> None:
        """
        Initializes a new node with the given data.

        Parameters
        ----------
        data : T
            The data to store in the node.
        """
        self.data: T = data
        self.next: Node[T] | None = None


class LinkedList(Generic[T]):
    """
    A singly Linked List data structure.

    Attributes
    ----------
    head : Node[T | None]
        The first node in the linked list.

    Methods
    -------
    append(data: T) -> None
        Adds a new node with the given data to the end of the list.
    prepend(data: T) -> None
        Adds a new node with the given data to the beginning of the list.
    delete(data: T) -> None
        Removes the first node containing the specified data.
    search(data: T) -> bool
        Searches for the first node containing the specified data.
    size() -> int
        Returns the number of nodes in the list.
    """

    def __init__(self) -> None:
        """
        Initializes an empty linked list.
        """
        self.head: Node[T] | None = None

    def append(self, data: T) -> None:
        """
        Adds a new node with the given data to the end of the list.

        Parameters
        ----------
        data : T
            The data to store in the new node.
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def prepend(self, data: T) -> None:
        """
        Adds a new node with the given data to the beginning of the list.

        Parameters
        ----------
        data : T
            The data to store in the new node.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data: T) -> None:
        """
        Removes the first node containing the specified data.

        Parameters
        ----------
        data : T
            The data to remove from the list.

        Raises
        ------
        ValueError
            If the data is not found in the list.
        """
        current = self.head
        if current and current.data == data:
            self.head = current.next
            return
        prev = None
        while current and current.data != data:
            prev = current
            current = current.next
        if not current:
            raise ValueError(f"Data {data} not found in the list")
        prev.next = current.next

    def search(self, data: T) -> bool:
        """
        Searches for the first node containing the specified data.

        Parameters
        ----------
        data : T
            The data to search for.

        Returns
        -------
        bool
            True if the data is found, False otherwise.
        """
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def size(self) -> int:
        """
        Returns the number of nodes in the list.

        Returns
        -------
        int
            The number of nodes in the list.
        """
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __iter__(self) -> Iterator[Node[T]]:
        current = self.head
        while current:
            yield current
            current = current.next
