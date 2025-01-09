from typing import List, Any

class Queue:
    """
    A Queue data structure.

    Attributes
    ----------
    items : List[Any]
        The list to store queue elements.

    Methods
    -------
    enqueue(item)
        Adds an element to the back of the queue.
    dequeue()
        Removes and returns the front element of the queue.
    is_empty()
        Checks if the queue is empty.
    size()
        Returns the number of elements in the queue.
    """

    def __init__(self) -> None:
        """
        Initializes an empty queue.
        """
        self.items: List[Any] = []

    def enqueue(self, item: Any) -> None:
        """
        Adds an element to the back of the queue.

        Parameters
        ----------
        item : Any
            The element to add to the queue.
        """
        self.items.append(item)

    def dequeue(self) -> Any:
        """
        Removes and returns the front element of the queue.

        Returns
        -------
        Any
            The front element of the queue.

        Raises
        ------
        IndexError
            If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        return self.items.pop(0)

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