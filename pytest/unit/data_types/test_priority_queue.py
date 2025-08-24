import pytest
from data_types.priority_queue import PriorityQueue


def test_push_and_pop() -> None:
    """
    Test case 1: Test adding and removing elements from the priority queue.
    """
    pq = PriorityQueue[int]()
    pq.push(10, 2)
    pq.push(20, 1)
    pq.push(30, 3)
    assert pq.pop() == 20  # Highest priority (lowest numerical value)
    assert pq.pop() == 10
    assert pq.pop() == 30


def test_is_empty() -> None:
    """
    Test case 2: Test checking if the priority queue is empty.
    """
    pq = PriorityQueue[int]()
    assert pq.is_empty() is True
    pq.push(10, 1)
    assert pq.is_empty() is False
    pq.pop()
    assert pq.is_empty() is True


def test_size() -> None:
    """
    Test case 3: Test getting the size of the priority queue.
    """
    pq = PriorityQueue[int]()
    assert pq.size() == 0
    pq.push(10, 1)
    pq.push(20, 2)
    assert pq.size() == 2
    pq.pop()
    assert pq.size() == 1
    pq.pop()
    assert pq.size() == 0


def test_priority_order() -> None:
    """
    Test case 4: Test that elements are returned in the correct priority order.
    """
    pq = PriorityQueue[str]()
    pq.push("low", 3)
    pq.push("medium", 2)
    pq.push("high", 1)
    assert pq.pop() == "high"  # Highest priority
    assert pq.pop() == "medium"
    assert pq.pop() == "low"


def test_duplicate_priorities() -> None:
    """
    Test case 5: Test handling of elements with duplicate priorities.
    """
    pq = PriorityQueue[str]()
    pq.push("first", 1)
    pq.push("second", 1)
    pq.push("third", 2)
    assert pq.pop() == "first"  # FIFO for same priority
    assert pq.pop() == "second"
    assert pq.pop() == "third"


def test_custom_object_priority_queue() -> None:

    """
    Test case 6: Test the priority queue with custom objects.
    """
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


def test_large_priority_queue() -> None:
    """
    Test case 7: Test operations on a very large priority queue.
    """
    pq = PriorityQueue[int]()
    for i in range(10000):
        pq.push(i, i)
    assert pq.size() == 10000
    assert pq.pop() == 0  # Lowest priority value
    assert pq.pop() == 1
    assert pq.size() == 9998


def test_order_of_elements() -> None:
    """
    Test case 8: Test the order of elements in the priority queue after multiple operations.
    """
    pq = PriorityQueue[int]()
    pq.push(10, 2)
    pq.push(20, 1)
    pq.push(30, 3)
    pq.pop()  # Remove the highest priority (20)
    pq.push(40, 0)  # Add a new highest priority
    elements = []
    while not pq.is_empty():
        elements.append(pq.pop())
    assert elements == [40, 10, 30]


def test_iterative_access() -> None:
    """
    Test case 9: Test iteration over the priority queue.
    """
    pq = PriorityQueue[int]()
    pq.push(10, 2)
    pq.push(20, 1)
    pq.push(30, 3)
    elements = sorted(pq.heap)  # Access the heap directly for testing
    assert elements == [(1, 20), (2, 10), (3, 30)]


def test_pop_empty_queue() -> None:
    """
    Test case 10: Test popping from an empty priority queue.
    """
    pq = PriorityQueue[int]()
    with pytest.raises(IndexError, match="Pop from an empty priority queue"):
        pq.pop()
