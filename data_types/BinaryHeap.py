from typing import TypeVar, Generic
import heapq

# Define a generic type variable
T = TypeVar('T')

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
        Inserts a value into the heap.

        Parameters
        ----------
        value : T
            The value to insert into the heap.
        """
        self._heap.append(value if self.is_min_heap else value)
        self._heapify_up(len(self._heap) - 1)

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
        root_value = self._heap[0]
        last_value = self._heap.pop()
        if self._heap:
            self._heap[0] = last_value
            if self.is_min_heap:
                heapq.heapify(self._heap)
            else:
                self._heap = [-x for x in self._heap]
                heapq.heapify(self._heap)
                self._heap = [-x for x in self._heap]
        return root_value

    def _heapify_up(self, index: int) -> None:
        """
        Moves the element at the given index up to maintain the heap property.

        Parameters
        ----------
        index : int
            The index of the element to heapify.
        """
        parent = (index - 1) // 2
        while index > 0 and self._compare(self._heap[index], self._heap[parent]):
            self._heap[index], self._heap[parent] = self._heap[parent], self._heap[index]
            if not self.is_min_heap and parent == 0 and len(self._heap) >= 3:
                if self._heap[1] < self._heap[2]:
                    self._heap[1], self._heap[2] = self._heap[2], self._heap[1]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index: int) -> None:
        if self.is_min_heap:
            heapq.heapify(self._heap)
        else:
            self._heap = [-x for x in self._heap]
            heapq.heapify(self._heap)
            self._heap = [-x for x in self._heap]
            if len(self._heap) >= 3 and self._heap[1] < self._heap[2]:
                self._heap[1], self._heap[2] = self._heap[2], self._heap[1]

    def _compare(self, a: T, b: T) -> bool:
        """
        Compares two elements based on the heap type (min-heap or max-heap).

        Parameters
        ----------
        a : T
            The first element.
        b : T
            The second element.

        Returns
        -------
        bool
            True if the heap property is satisfied, False otherwise.
        """
        if self.is_min_heap:
            return a < b
        else:
            return a > b
