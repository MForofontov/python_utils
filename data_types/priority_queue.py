import heapq
from typing import TypeVar, Generic

# Define a generic type variable
T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """
    A Priority Queue data structure using a min-heap.

    Attributes
    ----------
    heap : List[Tuple[int, T]]
        The list representing the heap, where each element is a tuple of (priority, value).

    Methods
    -------
    push(item: T, priority: int) -> None
        Adds an item with a given priority to the queue.
    pop() -> T
        Removes and returns the item with the highest priority (lowest numerical value).
    is_empty() -> bool
        Checks if the priority queue is empty.
    size() -> int
        Returns the number of elements in the priority queue.
    """

    def __init__(self) -> None:
        """
        Initializes an empty priority queue.
        """
        self.heap: list[tuple[int, T]] = []

    def push(self, item: T, priority: int) -> None:
        """
        Adds an item with a given priority to the queue.

        Parameters
        ----------
        item : T
            The item to be added to the queue.
        priority : int
            The priority of the item (lower values indicate higher priority).
        """
        heapq.heappush(self.heap, (priority, item))

    def pop(self) -> T:
        """
        Removes and returns the item with the highest priority.

        Returns
        -------
        T
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
