import pytest
from data_types.binary_heap import BinaryHeap


def test_insert_min_heap() -> None:
    """
    Test inserting elements into a min-heap.
    """
    # Test case 1: Insert into a min-heap
    heap = BinaryHeap[int](is_min_heap=True)  # Specify the type as int
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    assert heap.heap == [1, 5, 20, 10]  # Min-heap property should be maintained


def test_insert_max_heap() -> None:
    """
    Test inserting elements into a max-heap.
    """
    # Test case 2: Insert into a max-heap
    heap = BinaryHeap[int](is_min_heap=False)
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    assert heap.heap == [-20, -5, -10, -1]  # Internal representation uses negatives


def test_extract_min_heap() -> None:
    """
    Test extracting the root from a min-heap.
    """
    # Test case 3: Extract from a min-heap
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    root = heap.extract()
    assert root == 1  # Root should be the smallest element
    assert heap.heap == [5, 10, 20]  # Heap property should be maintained


def test_extract_max_heap() -> None:
    """
    Test extracting the root from a max-heap.
    """
    # Test case 4: Extract from a max-heap
    heap = BinaryHeap[int](is_min_heap=False)
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    heap.insert(1)
    root = heap.extract()
    assert root == 20  # Root should be the largest element
    assert heap.heap == [-10, -5, -1]  # Internal representation after extraction


def test_insert_and_extract_min_heap() -> None:
    """
    Test inserting and extracting elements from a min-heap.
    """
    # Test case 5: Insert and extract from a min-heap
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
    Test inserting and extracting elements from a max-heap.
    """
    # Test case 6: Insert and extract from a max-heap
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
    Test inserting and extracting a large number of elements.
    """
    # Test case 7: Large heap operations
    heap = BinaryHeap[int](is_min_heap=True)
    for i in range(100, 0, -1):  # Insert 100 to 1
        heap.insert(i)
    for i in range(1, 101):  # Extract 1 to 100
        assert heap.extract() == i
    assert heap.heap == []


def test_large_heap_operations_max_heap() -> None:
    """
    Test inserting and extracting a large number of elements in a max-heap.
    """
    # Test case 8: Large heap operations for max-heap
    heap = BinaryHeap[int](is_min_heap=False)
    for i in range(1, 101):  # Insert 1 to 100
        heap.insert(i)
    for i in range(100, 0, -1):  # Extract 100 to 1
        assert heap.extract() == i
    assert heap.heap == []


def test_insert_duplicate_elements_min_heap() -> None:
    """
    Test inserting duplicate elements into a min-heap.
    """
    # Test case 9: Insert duplicate elements into a min-heap
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(10)
    heap.insert(10)
    heap.insert(5)
    heap.insert(5)
    assert heap.heap == [5, 5, 10, 10]  # Min-heap property should be maintained


def test_insert_duplicate_elements_max_heap() -> None:
    """
    Test inserting duplicate elements into a max-heap.
    """
    # Test case 10: Insert duplicate elements into a max-heap
    heap = BinaryHeap[int](is_min_heap=False)
    heap.insert(10)
    heap.insert(10)
    heap.insert(20)
    heap.insert(20)
    assert heap.heap == [-20, -20, -10, -10]  # Internal representation uses negatives


def test_insert_boundary_values() -> None:
    """
    Test inserting boundary values into the heap.
    """
    # Test case 11: Insert boundary values
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(float("-inf"))
    heap.insert(float("inf"))
    assert heap.extract() == float("-inf")  # Smallest value for min-heap
    assert heap.extract() == float("inf")  # Largest value for min-heap


def test_extract_single_element() -> None:
    """
    Test extracting the only element from a heap.
    """
    # Test case 12: Extract the only element
    heap = BinaryHeap[int](is_min_heap=True)
    heap.insert(42)
    assert heap.extract() == 42
    assert heap.heap == []  # Heap should be empty


def test_heapify_min_heap() -> None:
    """
    Test heapifying a list into a min-heap.
    """
    # Test case 13: Heapify a list into a min-heap
    heap = BinaryHeap[int](is_min_heap=True)
    heap.heap = [10, 5, 20, 1]
    heap.heapify()
    assert heap.heap == [1, 5, 20, 10]  # Min-heap property should be maintained


def test_heapify_max_heap() -> None:
    """
    Test heapifying a list into a max-heap.
    """
    # Test case 14: Heapify a list into a max-heap
    heap = BinaryHeap[int](is_min_heap=False)
    heap.heap = [10, 5, 20, 1]
    heap.heapify()
    assert heap.heap == [-20, -5, -10, -1]  # Internal representation uses negatives


def test_extract_from_empty_heap() -> None:
    """
    Test extracting from an empty heap.
    """
    # Test case 15: Extract from an empty heap
    heap = BinaryHeap[int](is_min_heap=True)
    with pytest.raises(IndexError):
        heap.extract()  # Should raise an IndexError
