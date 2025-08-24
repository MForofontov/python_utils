
import pytest
from data_types.binary_heap import BinaryHeap


def test_insert_min_heap() -> None:
    """
    Test case 1: Test inserting elements into a min-heap.
    """
    heap = BinaryHeap[int](is_min_heap=True)  # Specify the type as int
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    # Min-heap property should be maintained
    assert heap.heap == [(1, 1), (5, 5), (20, 20), (10, 10)]


def test_insert_max_heap() -> None:
    """
    Test case 2: Test inserting elements into a max-heap.
    """
    heap = BinaryHeap[int](is_min_heap=False)
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    # Internal representation uses max-heap
    assert heap.heap == [(20, 20), (5, 5), (10, 10), (1, 1)]


def test_extract_min_heap() -> None:
    """
    Test case 3: Test extracting the root from a min-heap.
    """
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    root = heap.extract()
    assert root == 1  # Root should be the smallest element
    # Heap property should be maintained
    assert heap.heap == [(5, 5), (10, 10), (20, 20)]


def test_extract_max_heap() -> None:
    """
    Test case 4: Test extracting the root from a max-heap.
    """
    heap = BinaryHeap[int](is_min_heap=False)
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    root = heap.extract()
    assert root == 20  # Root should be the largest element
    # Internal representation after extraction
    assert heap.heap == [(10, 10), (5, 5), (1, 1)]


def test_insert_and_extract_min_heap() -> None:
    """
    Test case 5: Test inserting and extracting elements from a min-heap.
    """
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    assert heap.extract() == 1
    assert heap.extract() == 5
    assert heap.extract() == 10
    assert heap.extract() == 20
    assert heap.heap == []


def test_insert_and_extract_max_heap() -> None:
    """
    Test case 6: Test inserting and extracting elements from a max-heap.
    """
    heap = BinaryHeap[int](is_min_heap=False)
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    assert heap.extract() == 20
    assert heap.extract() == 10
    assert heap.extract() == 5
    assert heap.extract() == 1
    assert heap.heap == []


def test_large_heap_operations() -> None:
    """
    Test case 7: Test inserting and extracting a large number of elements.
    """
    heap = BinaryHeap[int](is_min_heap=True)
    for i in range(100, 0, -1):  # Insert 100 to 1
        heap.insert(i)
    for i in range(1, 101):  # Extract 1 to 100
        assert heap.extract() == i
    assert heap.heap == []


def test_large_heap_operations_max_heap() -> None:
    """
    Test case 8: Test inserting and extracting a large number of elements in a max-heap.
    """
    heap = BinaryHeap[int](is_min_heap=False)
    for i in range(1, 101):  # Insert 1 to 100
        heap.insert(i)
    for i in range(100, 0, -1):  # Extract 100 to 1
        assert heap.extract() == i
    assert heap.heap == []


def test_insert_duplicate_elements_min_heap() -> None:
    """
    Test case 9: Test inserting duplicate elements into a min-heap.
    """
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(10)
    heap.insert(10)
    heap.insert(5)
    heap.insert(5)
    # Min-heap property should be maintained
    assert heap.heap == [(5, 5), (5, 5), (10, 10), (10, 10)]


def test_insert_duplicate_elements_max_heap() -> None:
    """
    Test case 10: Test inserting duplicate elements into a max-heap.
    """
    heap = BinaryHeap[int](is_min_heap=False)
    heap.insert(10)
    heap.insert(10)
    heap.insert(20)
    heap.insert(20)
    # Internal representation uses max-heap
    assert heap.heap == [(20, 20), (20, 20), (10, 10), (10, 10)]


def test_insert_boundary_values() -> None:
    """
    Test case 11: Test inserting boundary values into the heap.
    """
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(float("-inf"))
    heap.insert(float("inf"))
    assert heap.extract() == float("-inf")  # Smallest value for min-heap
    assert heap.extract() == float("inf")  # Largest value for min-heap


def test_extract_single_element() -> None:
    """
    Test case 12: Test extracting the only element from a heap.
    """
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(42)
    assert heap.extract() == 42
    assert heap.heap == []  # Heap should be empty


def test_heapify_min_heap() -> None:
    """
    Test case 13: Test heapifying a list into a min-heap.
    """
    heap = BinaryHeap[int](is_min_heap=True)
    heap.heap = [(10, 10), (5, 5), (20, 20), (1, 1)]
    heap.heapify()
    # Min-heap property should be maintained
    assert heap.heap == [(1, 1), (5, 5), (20, 20), (10, 10)]


def test_heapify_max_heap() -> None:
    """
    Test case 14: Test heapifying a list into a max-heap.
    """
    heap = BinaryHeap[int](is_min_heap=False)
    heap.heap = [(10, 10), (5, 5), (20, 20), (1, 1)]
    heap.heapify()
    # Internal representation uses max-heap
    assert heap.heap == [(20, 20), (5, 5), (10, 10), (1, 1)]


def test_extract_from_empty_heap() -> None:
    """
    Test case 15: Test extracting from an empty heap.
    """
    heap = BinaryHeap[int](is_min_heap=True)
    with pytest.raises(IndexError):
        heap.extract()  # Should raise an IndexError


def test_non_numeric_min_heap() -> None:
    """Ensure heap handles non-numeric values in a min-heap."""
    heap = BinaryHeap[str](is_min_heap=True)
    heap.insert("banana", priority=2)
    heap.insert("apple", priority=1)
    heap.insert("cherry", priority=3)
    assert heap.extract() == "apple"
    assert heap.extract() == "banana"
    assert heap.extract() == "cherry"


def test_non_numeric_max_heap() -> None:
    """Ensure heap handles non-numeric values in a max-heap."""
    heap = BinaryHeap[str](is_min_heap=False)
    heap.insert("banana", priority=2)
    heap.insert("apple", priority=1)
    heap.insert("cherry", priority=3)
    assert heap.extract() == "cherry"
    assert heap.extract() == "banana"
    assert heap.extract() == "apple"
