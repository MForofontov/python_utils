import pytest
from data_types.BinaryHeap import BinaryHeap

def test_insert_min_heap():
    """
    Test the insert method for a min-heap.
    """
    heap = BinaryHeap(is_min_heap=True)
    heap.insert(10)
    heap.insert(5)
    heap.insert(15)
    heap.insert(3)
    assert heap.heap == [3, 5, 15, 10], "Min-heap property violated after insert"

def test_insert_max_heap():
    """
    Test the insert method for a max-heap.
    """
    heap = BinaryHeap(is_min_heap=False)
    heap.insert(10)
    heap.insert(5)
    heap.insert(15)
    heap.insert(3)
    assert heap.heap == [15, 10, 5, 3], "Max-heap property violated after insert"

def test_extract_min_heap():
    """
    Test the extract method for a min-heap.
    """
    heap = BinaryHeap(is_min_heap=True)
    for value in [10, 5, 15, 3]:
        heap.insert(value)
    assert heap.extract() == 3, "Failed to extract the smallest element"
    assert heap.extract() == 5, "Failed to extract the next smallest element"
    assert heap.extract() == 10, "Failed to extract the next smallest element"
    assert heap.extract() == 15, "Failed to extract the largest element"
    with pytest.raises(IndexError):
        heap.extract()  # Extracting from an empty heap

def test_extract_max_heap():
    """
    Test the extract method for a max-heap.
    """
    heap = BinaryHeap(is_min_heap=False)
    for value in [10, 5, 15, 3]:
        heap.insert(value)
    assert heap.extract() == 15, "Failed to extract the largest element"
    assert heap.extract() == 10, "Failed to extract the next largest element"
    assert heap.extract() == 5, "Failed to extract the next largest element"
    assert heap.extract() == 3, "Failed to extract the smallest element"
    with pytest.raises(IndexError):
        heap.extract()  # Extracting from an empty heap

def test_heapify_up_min_heap():
    """
    Test the _heapify_up method for a min-heap.
    """
    heap = BinaryHeap(is_min_heap=True)
    heap.heap = [10, 20, 15, 5]
    heap._heapify_up(3)
    assert heap.heap == [5, 10, 15, 20], "Min-heap property violated after _heapify_up"

def test_heapify_up_max_heap():
    """
    Test the _heapify_up method for a max-heap.
    """
    heap = BinaryHeap(is_min_heap=False)
    heap.heap = [10, 5, 15, 20]
    heap._heapify_up(3)
    assert heap.heap == [20, 10, 15, 5], "Max-heap property violated after _heapify_up"

def test_heapify_down_min_heap():
    """
    Test the _heapify_down method for a min-heap.
    """
    heap = BinaryHeap(is_min_heap=True)
    heap.heap = [20, 10, 15, 5]
    heap._heapify_down(0)
    assert heap.heap == [10, 5, 15, 20], "Min-heap property violated after _heapify_down"

def test_heapify_down_max_heap():
    """
    Test the _heapify_down method for a max-heap.
    """
    heap = BinaryHeap(is_min_heap=False)
    heap.heap = [5, 20, 15, 10]
    heap._heapify_down(0)
    assert heap.heap == [20, 10, 15, 5], "Max-heap property violated after _heapify_down"

def test_compare_min_heap():
    """
    Test the _compare method for a min-heap.
    """
    heap = BinaryHeap(is_min_heap=True)
    assert heap._compare(5, 10) is True, "Min-heap comparison failed"
    assert heap._compare(10, 5) is False, "Min-heap comparison failed"

def test_compare_max_heap():
    """
    Test the _compare method for a max-heap.
    """
    heap = BinaryHeap(is_min_heap=False)
    assert heap._compare(10, 5) is True, "Max-heap comparison failed"
    assert heap._compare(5, 10) is False, "Max-heap comparison failed"

def test_empty_heap_extraction():
    """
    Test extracting from an empty heap.
    """
    heap = BinaryHeap(is_min_heap=True)
    with pytest.raises(IndexError):
        heap.extract()

def test_large_numbers():
    """
    Test the heap with very large numbers.
    """
    heap = BinaryHeap(is_min_heap=True)
    heap.insert(10**6)
    heap.insert(10**9)
    heap.insert(10**3)
    assert heap.extract() == 10**3, "Failed to extract smallest large number"
    assert heap.extract() == 10**6, "Failed to extract next smallest large number"
    assert heap.extract() == 10**9, "Failed to extract largest large number"