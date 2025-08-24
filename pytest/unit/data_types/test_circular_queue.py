import pytest
from data_types.circular_queue import CircularQueue


def test_enqueue_to_empty_queue() -> None:
    """
    Test case 1: Test enqueuing an item to an empty queue.
    """
    queue = CircularQueue[int](3)  # Specify the type as int
    assert queue.enqueue(10) is True
    assert queue.peek() == 10
    assert queue.size() == 1


def test_enqueue_to_full_queue() -> None:
    """
    Test case 2: Test enqueuing an item to a full queue.
    """
    queue = CircularQueue[int](3)
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    assert queue.enqueue(40) is False  # Queue is full
    assert queue.size() == 3


def test_dequeue_from_empty_queue() -> None:
    """
    Test case 3: Test dequeuing an item from an empty queue.
    """
    queue = CircularQueue[int](3)
    assert queue.dequeue() is None  # Queue is empty


def test_dequeue_from_non_empty_queue() -> None:
    """
    Test case 4: Test dequeuing an item from a non-empty queue.
    """
    queue = CircularQueue[int](3)
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.dequeue() == 10  # Dequeue the first item
    assert queue.size() == 1
    assert queue.peek() == 20


def test_peek_empty_queue() -> None:
    """
    Test case 5: Test peeking into an empty queue.
    """
    queue = CircularQueue[int](3)
    assert queue.peek() is None  # Queue is empty


def test_peek_non_empty_queue() -> None:
    """
    Test case 6: Test peeking into a non-empty queue.
    """
    queue = CircularQueue[int](3)
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.peek() == 10  # Peek should return the first item
    assert queue.size() == 2  # Size should remain unchanged


def test_is_empty_on_empty_queue() -> None:
    """
    Test case 7: Test checking if an empty queue is empty.
    """
    queue = CircularQueue[int](3)
    assert queue.is_empty() is True


def test_is_empty_on_non_empty_queue() -> None:
    """
    Test case 8: Test checking if a non-empty queue is empty.
    """
    queue = CircularQueue[int](3)
    queue.enqueue(10)
    assert queue.is_empty() is False


def test_is_full_on_full_queue() -> None:
    """
    Test case 9: Test checking if a full queue is full.
    """
    queue = CircularQueue[int](3)
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    assert queue.is_full() is True


def test_is_full_on_non_full_queue() -> None:
    """
    Test case 10: Test checking if a non-full queue is full.
    """
    queue = CircularQueue[int](3)
    queue.enqueue(10)
    assert queue.is_full() is False


def test_circular_behavior() -> None:
    """
    Test case 11: Test the circular behavior of the queue.
    """
    queue = CircularQueue[int](3)
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
    Test case 12: Test enqueuing and dequeuing multiple times to ensure circular behavior.
    """
    queue = CircularQueue[int](3)
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
    Test case 13: Test filling the queue completely, then dequeuing all items.
    """
    queue = CircularQueue[int](3)
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
    Test case 14: Test peeking after enqueuing and dequeuing items.
    """
    queue = CircularQueue[int](3)
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.dequeue() == 10
    assert queue.peek() == 20  # Peek should return the next front item
    queue.enqueue(30)
    assert queue.peek() == 20  # Peek should still return the front item


def test_size_after_multiple_operations() -> None:
    """
    Test case 15: Test the size of the queue after multiple enqueue and dequeue operations.
    """
    queue = CircularQueue[int](3)
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
    Test case 16: Test enqueuing after dequeuing all items to empty the queue.
    """
    queue = CircularQueue[int](3)
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


def test_queue_with_zero_size() -> None:
    """
    Test case 17: Test initializing a CircularQueue with a size of 0.
    """
    with pytest.raises(ValueError, match="Queue size must be greater than 0"):
        CircularQueue[int](0)  # Zero size is not allowed
