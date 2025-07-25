from typing import TypeVar, Generic
import heapq

# Define a generic type variable
T = TypeVar("T")


class BinaryHeap(Generic[T]):
    """
    A Binary Heap data structure.

    Attributes
    ----------
    heap : List[T]
        A list representing the binary heap.
    is_min_heap : bool
        A flag indicating whether it's a min-heap or max-heap.

    Methods
    -------
    insert(value: T) -> None
        Inserts a value into the heap.
    extract() -> T
        Extracts the root value (min or max) from the heap.
    heapify() -> None
        Converts the list into a valid heap.
    """

    def __init__(self, is_min_heap: bool = True) -> None:
        self._heap: list[T] = []
        self.is_min_heap: bool = is_min_heap

    @property
    def heap(self) -> list[T]:
        return self._heap

    @heap.setter
    def heap(self, values: list[T]) -> None:
        self._heap = values

    def insert(self, value: T) -> None:
        """
        Inserts a value into the heap using ``heapq.heappush``.

        Parameters
        ----------
        value : T
            The value to insert into the heap.
        """
        heapq.heappush(self._heap, value if self.is_min_heap else -value)

    def extract(self) -> T:
        """
        Extracts the root value (min or max) from the heap.

        Returns
        -------
        T
            The root value of the heap.

        Raises
        ------
        IndexError
            If the heap is empty.
        """
        if len(self._heap) == 0:
            raise IndexError("extract from empty heap")
        value = heapq.heappop(self._heap)
        return value if self.is_min_heap else -value

    def heapify(self) -> None:
        """Converts the current list into a valid heap."""
        if self.is_min_heap:
            heapq.heapify(self._heap)
        else:
            self._heap = [-x for x in self._heap]
            heapq.heapify(self._heap)
