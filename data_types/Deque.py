from typing import List, TypeVar, Generic

# Define a generic type variable
T = TypeVar('T')

class Deque(Generic[T]):
    """
    A Deque (Double-Ended Queue) data structure.

    Attributes
    ----------
    items : List[T]
        The list to store deque elements.

    Methods
    -------
    add_front(item: T) -> None
        Adds an element to the front of the deque.
    add_rear(item: T) -> None
        Adds an element to the rear of the deque.
    remove_front() -> T
        Removes and returns the front element of the deque.
    remove_rear() -> T
        Removes and returns the rear element of the deque.
    is_empty() -> bool
        Checks if the deque is empty.
    size() -> int
        Returns the number of elements in the deque.
    """

    def __init__(self) -> None:
        """
        Initializes an empty deque.
        """
        self.items: List[T] = []

    def add_front(self, item: T) -> None:
        """
        Adds an element to the front of the deque.

        Parameters
        ----------
        item : T
            The element to add to the deque.
        """
        self.items.insert(0, item)

    def add_rear(self, item: T) -> None:
        """
        Adds an element to the rear of the deque.

        Parameters
        ----------
        item : T
            The element to add to the deque.
        """
        self.items.append(item)

    def remove_front(self) -> T:
        """
        Removes and returns the front element of the deque.

        Returns
        -------
        T
            The front element of the deque.

        Raises
        ------
        IndexError
            If the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Remove from an empty deque")
        return self.items.pop(0)

    def remove_rear(self) -> T:
        """
        Removes and returns the rear element of the deque.

        Returns
        -------
        T
            The rear element of the deque.

        Raises
        ------
        IndexError
            If the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Remove from an empty deque")
        return self.items.pop()

    def is_empty(self) -> bool:
        """
        Checks if the deque is empty.

        Returns
        -------
        bool
            True if the deque is empty, False otherwise.
        """
        return len(self.items) == 0

    def size(self) -> int:
        """
        Returns the number of elements in the deque.

        Returns
        -------
        int
            The number of elements in the deque.
        """
        return len(self.items)
