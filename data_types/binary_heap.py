from typing import Generic, TypeVar
import heapq

# Define a generic type variable for the stored value
T = TypeVar("T")


class BinaryHeap(Generic[T]):
    """Binary Heap storing items as ``(priority, value)`` tuples.

    The heap maintains items as ``(priority, value)`` pairs where ``priority``
    is a numeric value used to determine ordering and ``value`` is any type.
    When ``is_min_heap`` is ``True`` (default), the smallest priority is at the
    root. For a max-heap (``is_min_heap=False``), the largest priority is at the
    root using ``heapq``'s max-heap helpers—no numeric negation of values is
    required.

    Parameters
    ----------
    is_min_heap : bool, optional
        If ``True`` the heap behaves as a min-heap, otherwise as a max-heap.

    Notes
    -----
    ``priority`` should be a numeric type (``int`` or ``float``). If ``priority``
    is omitted during insertion the provided ``value`` must itself be numeric and
    will be used as the priority. A priority must be supplied for non-numeric
    values.
    """

    def __init__(self, is_min_heap: bool = True) -> None:
        self._heap: list[tuple[int | float, T]] = []
        self.is_min_heap: bool = is_min_heap

    @property
    def heap(self) -> list[tuple[int | float, T]]:
        return self._heap

    @heap.setter
    def heap(self, values: list[tuple[int | float, T]]) -> None:
        self._heap = values

    def insert(self, value: T, priority: float | None = None) -> None:
        """Insert ``value`` with the given ``priority``.

        Parameters
        ----------
        value : T
            The value to insert into the heap.
        priority : float | None, optional
            Numeric priority for the value. If ``None`` the ``value`` must be
            numeric and will be used as the priority.
        """
        if priority is None:
            if not isinstance(value, (int, float)):
                raise TypeError(
                    "Priority must be provided for non-numeric values")
            priority = value
        item = (priority, value)
        if self.is_min_heap:
            heapq.heappush(self._heap, item)
        else:
            self._heap.append(item)
            heapq._siftdown_max(self._heap, 0, len(self._heap) - 1)

    def extract(self) -> T:
        """Extract the root value (min or max) from the heap.

        Returns
        -------
        T
            The value with the highest priority.

        Raises
        ------
        IndexError
            If the heap is empty.
        """
        if len(self._heap) == 0:
            raise IndexError("extract from empty heap")
        if self.is_min_heap:
            _, value = heapq.heappop(self._heap)
        else:
            _, value = heapq._heappop_max(self._heap)
        return value

    def heapify(self) -> None:
        """Convert the current list of ``(priority, value)`` pairs into a heap."""
        if self.is_min_heap:
            heapq.heapify(self._heap)
        else:
            heapq._heapify_max(self._heap)
