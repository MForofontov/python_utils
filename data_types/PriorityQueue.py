import heapq
from typing import Any, Tuple, List

class PriorityQueue:
    """
    A Priority Queue data structure using a min-heap.

    Attributes
    ----------
    heap : List[Tuple[int, Any]]
        The list representing the heap, where each element is a tuple of (priority, value).

    Methods
    -------
    push(item, priority)
        Adds an item with a given priority to the queue.
    pop()
        Removes and returns the item with the highest priority (lowest numerical value).
    is_empty()
        Checks if the priority queue is empty.
    size()
        Returns the number of elements in the priority queue.
    """

    def __init__(self) -> None:
        """
        Initializes an empty priority queue.
        """
        self.heap: List[Tuple[int, Any]] = []

    def push(self, item: Any, priority: int) -> None:
        """
        Adds an item with a given priority to the queue.

        Parameters
        ----------
        item : Any
            The item to be added to the queue.
        priority : int
            The priority of the item (lower values indicate higher priority).
        """
        heapq.heappush(self.heap, (priority, item))

    def pop(self) -> Any:
        """
        Removes and returns the item with the highest priority.

        Returns
        -------
        Any
            The item with the highest priority.

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty priority queue")
        return heapq.heappop(self.heap)[1]

    def is_empty(self) -> bool:
        """
        Checks if the priority queue is empty.

        Returns
        -------
        bool
            True if the priority queue is empty, False otherwise.
        """
        return len(self.heap) == 0

    def size(self) -> int:
        """
        Returns the number of elements in the priority queue.

        Returns
        -------
        int
            The number of elements in the priority queue.
        """
        return len(self.heap)
