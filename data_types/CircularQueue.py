from typing import Any, Optional

class CircularQueue:
    """
    A Circular Queue data structure.

    Attributes
    ----------
    size : int
        The maximum number of items the queue can hold.
    queue : list[Optional[Any]]
        The list of items in the queue.
    front : int
        The index of the front of the queue.
    rear : int
        The index of the rear of the queue.

    Methods
    -------
    enqueue(item: Any) -> bool
        Adds an item to the queue.
    dequeue() -> Optional[Any]
        Removes and returns the front item of the queue.
    peek() -> Optional[Any]
        Returns the front item without removing it.
    is_empty() -> bool
        Checks if the queue is empty.
    is_full() -> bool
        Checks if the queue is full.
    size() -> int
        Returns the current number of items in the queue.
    """

    def __init__(self, size: int) -> None:
        self.size: int = size
        self.queue: list[Optional[Any]] = [None] * size
        self.front: int = -1
        self.rear: int = -1

    def enqueue(self, item: Any) -> bool:
        """
        Adds an item to the queue.

        Parameters
        ----------
        item : Any
            The item to add to the queue.

        Returns
        -------
        bool
            True if the item was added, False if the queue is full.
        """
        if self.is_full():
            return False
        if self.front == -1:
            self.front = 0
        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = item
        return True

    def dequeue(self) -> Optional[Any]:
        """
        Removes and returns the front item of the queue.

        Returns
        -------
        Optional[Any]
            The front item of the queue, or None if the queue is empty.
        """
        if self.is_empty():
            return None
        item = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.size
        return item

    def peek(self) -> Optional[Any]:
        """
        Returns the front item without removing it.

        Returns
        -------
        Optional[Any]
            The front item of the queue, or None if the queue is empty.
        """
        if self.is_empty():
            return None
        return self.queue[self.front]

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.

        Returns
        -------
        bool
            True if the queue is empty, False otherwise.
        """
        return self.front == -1

    def is_full(self) -> bool:
        """
        Checks if the queue is full.

        Returns
        -------
        bool
            True if the queue is full, False otherwise.
        """
        return (self.rear + 1) % self.size == self.front

    def size(self) -> int:
        """
        Returns the current number of items in the queue.

        Returns
        -------
        int
            The number of items in the queue.
        """
        if self.is_empty():
            return 0
        return (self.rear - self.front + 1) % self.size
