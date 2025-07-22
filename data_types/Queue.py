from typing import TypeVar, Generic
from collections import deque

# Define a generic type variable
T = TypeVar('T')

class Queue(Generic[T]):
    """
    A Queue data structure built on :class:`collections.deque`.
    All queue operations run in constant time.

    Attributes
    ----------
    items : deque[T]
        A deque to store queue elements. Operations from the front or
        back run in constant time.

    Methods
    -------
    enqueue(item: T) -> None
        Adds an element to the back of the queue.
    dequeue() -> T
        Removes and returns the front element of the queue.
    is_empty() -> bool
        Checks if the queue is empty.
    size() -> int
        Returns the number of elements in the queue.
    """

    def __init__(self) -> None:
        """
        Initializes an empty queue.
        """
        self.items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        """
        Adds an element to the back of the queue.

        Parameters
        ----------
        item : T
            The element to add to the queue.
        """
        self.items.append(item)

    def dequeue(self) -> T:
        """
        Removes and returns the front element of the queue.

        Returns
        -------
        T
            The front element of the queue.

        Raises
        ------
        IndexError
            If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        return self.items.popleft()

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.

        Returns
        -------
        bool
            True if the queue is empty, False otherwise.
        """
        return len(self.items) == 0

    def size(self) -> int:
        """
        Returns the number of elements in the queue.

        Returns
        -------
        int
            The number of elements in the queue.
        """
        return len(self.items)
