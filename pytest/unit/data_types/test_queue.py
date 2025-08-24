import pytest
from data_types.queue import Queue


def test_enqueue_and_dequeue() -> None:
    """
    Test case 1: Test adding and removing elements from the queue.
    """
    queue = Queue[int]()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    assert queue.dequeue() == 1  # First in, first out
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3


def test_is_empty() -> None:
    """
    Test case 2: Test checking if the queue is empty.
    """
    queue = Queue[int]()
    assert queue.is_empty() is True
    queue.enqueue(1)
    assert queue.is_empty() is False
    queue.dequeue()
    assert queue.is_empty() is True


def test_size() -> None:
    """
    Test case 3: Test getting the size of the queue.
    """
    queue = Queue[int]()
    assert queue.size() == 0
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.size() == 2
    queue.dequeue()
    assert queue.size() == 1
    queue.dequeue()
    assert queue.size() == 0


def test_order_of_elements() -> None:
    """
    Test case 4: Test the order of elements in the queue after multiple operations.
    """
    queue = Queue[int]()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.dequeue()  # Remove the first element (1)
    queue.enqueue(4)  # Add a new element
    elements = []
    while not queue.is_empty():
        elements.append(queue.dequeue())
    assert elements == [2, 3, 4]


def test_custom_object_queue() -> None:

    """
    Test case 5: Test the queue with custom objects.
    """
    class Task:
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return f"Task({self.name})"

    queue = Queue[Task]()
    task1 = Task("Task1")
    task2 = Task("Task2")
    task3 = Task("Task3")
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)
    assert queue.dequeue() == task1  # First in, first out
    assert queue.dequeue() == task2
    assert queue.dequeue() == task3


def test_large_queue() -> None:
    """
    Test case 6: Test operations on a very large queue.
    """
    queue = Queue[int]()
    for i in range(10000):
        queue.enqueue(i)
    assert queue.size() == 10000
    assert queue.dequeue() == 0  # First element
    assert queue.dequeue() == 1
    assert queue.size() == 9998


def test_single_element_queue() -> None:
    """
    Test case 7: Test enqueuing and dequeuing a single element.
    """
    queue = Queue[int]()
    queue.enqueue(42)
    assert queue.size() == 1
    assert queue.dequeue() == 42
    assert queue.is_empty() is True


def test_iterative_access() -> None:
    """
    Test case 8: Test iteration over the queue.
    """
    queue = Queue[int]()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    # Access the queue's items directly
    elements = [item for item in queue.items]
    assert elements == [1, 2, 3]


def test_dequeue_empty_queue() -> None:
    """
    Test case 9: Test removing an element from an empty queue.
    """
    queue = Queue[int]()
    with pytest.raises(IndexError, match="Dequeue from an empty queue"):
        queue.dequeue()
