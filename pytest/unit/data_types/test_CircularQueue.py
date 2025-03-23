import pytest
from data_types.CircularQueue import CircularQueue

def test_enqueue_to_empty_queue() -> None:
    """
    Test enqueuing an item to an empty queue.
    """
    # Test case 1: Enqueue to an empty queue
    queue = CircularQueue(3)
    assert queue.enqueue(10) is True
    assert queue.peek() == 10
    assert queue.size() == 1

def test_enqueue_to_full_queue() -> None:
    """
    Test enqueuing an item to a full queue.
    """
    # Test case 2: Enqueue to a full queue
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    assert queue.enqueue(40) is False  # Queue is full
    assert queue.size() == 3

def test_dequeue_from_empty_queue() -> None:
    """
    Test dequeuing an item from an empty queue.
    """
    # Test case 3: Dequeue from an empty queue
    queue = CircularQueue(3)
    assert queue.dequeue() is None  # Queue is empty

def test_dequeue_from_non_empty_queue() -> None:
    """
    Test dequeuing an item from a non-empty queue.
    """
    # Test case 4: Dequeue from a non-empty queue
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.dequeue() == 10  # Dequeue the first item
    assert queue.size() == 1
    assert queue.peek() == 20

def test_peek_empty_queue() -> None:
    """
    Test peeking into an empty queue.
    """
    # Test case 5: Peek into an empty queue
    queue = CircularQueue(3)
    assert queue.peek() is None  # Queue is empty

def test_peek_non_empty_queue() -> None:
    """
    Test peeking into a non-empty queue.
    """
    # Test case 6: Peek into a non-empty queue
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.peek() == 10  # Peek should return the first item
    assert queue.size() == 2  # Size should remain unchanged

def test_is_empty_on_empty_queue() -> None:
    """
    Test checking if an empty queue is empty.
    """
    # Test case 7: Check is_empty on an empty queue
    queue = CircularQueue(3)
    assert queue.is_empty() is True

def test_is_empty_on_non_empty_queue() -> None:
    """
    Test checking if a non-empty queue is empty.
    """
    # Test case 8: Check is_empty on a non-empty queue
    queue = CircularQueue(3)
    queue.enqueue(10)
    assert queue.is_empty() is False

def test_is_full_on_full_queue() -> None:
    """
    Test checking if a full queue is full.
    """
    # Test case 9: Check is_full on a full queue
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    assert queue.is_full() is True

def test_is_full_on_non_full_queue() -> None:
    """
    Test checking if a non-full queue is full.
    """
    # Test case 10: Check is_full on a non-full queue
    queue = CircularQueue(3)
    queue.enqueue(10)
    assert queue.is_full() is False

def test_circular_behavior() -> None:
    """
    Test the circular behavior of the queue.
    """
    # Test case 11: Circular behavior
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    assert queue.dequeue() == 10  # Remove the first item
    assert queue.enqueue(40) is True  # Add a new item
    assert queue.peek() == 20  # The front should now be 20
    assert queue.size() == 3  # Queue should still be full
    assert queue.is_full() is True

def test_enqueue_and_dequeue_multiple_times() -> None:
    """
    Test enqueuing and dequeuing multiple times to ensure circular behavior.
    """
    # Test case 12: Enqueue and dequeue multiple times
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    assert queue.dequeue() == 10  # Remove the first item
    assert queue.dequeue() == 20  # Remove the second item
    queue.enqueue(40)
    queue.enqueue(50)
    assert queue.dequeue() == 30  # Remove the third item
    assert queue.dequeue() == 40  # Remove the fourth item
    assert queue.dequeue() == 50  # Remove the fifth item
    assert queue.is_empty() is True  # Queue should now be empty

def test_enqueue_to_full_then_dequeue_all() -> None:
    """
    Test filling the queue completely, then dequeuing all items.
    """
    # Test case 13: Enqueue to full, then dequeue all
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    assert queue.is_full() is True
    assert queue.dequeue() == 10
    assert queue.dequeue() == 20
    assert queue.dequeue() == 30
    assert queue.is_empty() is True

def test_peek_after_enqueue_and_dequeue() -> None:
    """
    Test peeking after enqueuing and dequeuing items.
    """
    # Test case 14: Peek after enqueue and dequeue
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.dequeue() == 10
    assert queue.peek() == 20  # Peek should return the next front item
    queue.enqueue(30)
    assert queue.peek() == 20  # Peek should still return the front item

def test_size_after_multiple_operations() -> None:
    """
    Test the size of the queue after multiple enqueue and dequeue operations.
    """
    # Test case 15: Size after multiple operations
    queue = CircularQueue(3)
    assert queue.size() == 0  # Initially empty
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.size() == 2  # Two items in the queue
    queue.dequeue()
    assert queue.size() == 1  # One item left
    queue.enqueue(30)
    queue.enqueue(40)
    assert queue.size() == 3  # Queue is full
    queue.dequeue()
    queue.dequeue()
    assert queue.size() == 1  # One item left

def test_enqueue_after_dequeue_empty() -> None:
    """
    Test enqueuing after dequeuing all items to empty the queue.
    """
    # Test case 16: Enqueue after dequeue empty
    queue = CircularQueue(3)
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    queue.dequeue()
    queue.dequeue()
    queue.dequeue()
    assert queue.is_empty() is True  # Queue is empty
    assert queue.enqueue(40) is True  # Enqueue after emptying
    assert queue.peek() == 40
    assert queue.size() == 1
