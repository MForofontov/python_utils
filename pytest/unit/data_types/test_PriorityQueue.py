import pytest
from data_types.PriorityQueue import PriorityQueue

def test_push_and_pop() -> None:
    """
    Test adding and removing elements from the priority queue.
    """
    # Test case 1: Push and pop elements
    pq = PriorityQueue[int]()
    pq.push(10, 2)
    pq.push(20, 1)
    pq.push(30, 3)
    assert pq.pop() == 20  # Highest priority (lowest numerical value)
    assert pq.pop() == 10
    assert pq.pop() == 30

def test_is_empty() -> None:
    """
    Test checking if the priority queue is empty.
    """
    # Test case 2: Empty queue
    pq = PriorityQueue[int]()
    assert pq.is_empty() is True
    pq.push(10, 1)
    assert pq.is_empty() is False
    pq.pop()
    assert pq.is_empty() is True

def test_size() -> None:
    """
    Test getting the size of the priority queue.
    """
    # Test case 3: Size of the queue
    pq = PriorityQueue[int]()
    assert pq.size() == 0
    pq.push(10, 1)
    pq.push(20, 2)
    assert pq.size() == 2
    pq.pop()
    assert pq.size() == 1
    pq.pop()
    assert pq.size() == 0

def test_pop_empty_queue() -> None:
    """
    Test popping from an empty priority queue.
    """
    # Test case 4: Pop from empty queue
    pq = PriorityQueue[int]()
    with pytest.raises(IndexError, match="Pop from an empty priority queue"):
        pq.pop()

def test_priority_order() -> None:
    """
    Test that elements are returned in the correct priority order.
    """
    # Test case 5: Priority order
    pq = PriorityQueue[str]()
    pq.push("low", 3)
    pq.push("medium", 2)
    pq.push("high", 1)
    assert pq.pop() == "high"  # Highest priority
    assert pq.pop() == "medium"
    assert pq.pop() == "low"

def test_duplicate_priorities() -> None:
    """
    Test handling of elements with duplicate priorities.
    """
    # Test case 6: Duplicate priorities
    pq = PriorityQueue[str]()
    pq.push("first", 1)
    pq.push("second", 1)
    pq.push("third", 2)
    assert pq.pop() == "first"  # FIFO for same priority
    assert pq.pop() == "second"
    assert pq.pop() == "third"

def test_custom_object_priority_queue() -> None:
    """
    Test the priority queue with custom objects.
    """
    # Test case 7: Custom objects
    class Task:
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return f"Task({self.name})"

    pq = PriorityQueue[Task]()
    task1 = Task("Task1")
    task2 = Task("Task2")
    task3 = Task("Task3")
    pq.push(task1, 3)
    pq.push(task2, 1)
    pq.push(task3, 2)
    assert pq.pop() == task2  # Highest priority
    assert pq.pop() == task3
    assert pq.pop() == task1