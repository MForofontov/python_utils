from typing import List, Any

class Deque:
    """
    A Deque (Double-Ended Queue) data structure.

    Attributes
    ----------
    items : List[Any]
        The list to store deque elements.

    Methods
    -------
    add_front(item)
        Adds an element to the front of the deque.
    add_rear(item)
        Adds an element to the rear of the deque.
    remove_front()
        Removes and returns the front element of the deque.
    remove_rear()
        Removes and returns the rear element of the deque.
    is_empty()
        Checks if the deque is empty.
    size()
        Returns the number of elements in the deque.
    """

    def __init__(self) -> None:
        """
        Initializes an empty deque.
        """
        self.items: List[Any] = []

    def add_front(self, item: Any) -> None:
        """
        Adds an element to the front of the deque.

        Parameters
        ----------
        item : Any
            The element to add to the deque.
        """
        self.items.insert(0, item)

    def add_rear(self, item: Any) -> None:
        """
        Adds an element to the rear of the deque.

        Parameters
        ----------
        item : Any
            The element to add to the deque.
        """
        self.items.append(item)

    def remove_front(self) -> Any:
        """
        Removes and returns the front element of the deque.

        Returns
        -------
        Any
            The front element of the deque.

        Raises
        ------
        IndexError
            If the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Remove from an empty deque")
        return self.items.pop(0)

    def remove_rear(self) -> Any:
        """
        Removes and returns the rear element of the deque.

        Returns
        -------
        Any
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
