import pytest
from data_types.deque import Deque


def test_add_front() -> None:
    """
    Test case 1: Test adding elements to the front of the deque.
    """
    deque = Deque[int]()
    deque.add_front(10)
    deque.add_front(20)
    assert list(deque.items) == [
        20,
        10,
    ]  # The most recent element should be at the front


def test_add_rear() -> None:
    """
    Test case 2: Test adding elements to the rear of the deque.
    """
    deque = Deque[int]()
    deque.add_rear(10)
    deque.add_rear(20)
    assert list(deque.items) == [
        10,
        20,
    ]  # The most recent element should be at the rear


def test_remove_front() -> None:
    """
    Test case 3: Test removing elements from the front of the deque.
    """
    deque = Deque[int]()
    deque.add_front(10)
    deque.add_front(20)
    assert deque.remove_front() == 20  # The front element should be removed
    assert list(deque.items) == [10]


def test_remove_rear() -> None:
    """
    Test case 4: Test removing elements from the rear of the deque.
    """
    deque = Deque[int]()
    deque.add_rear(10)
    deque.add_rear(20)
    assert deque.remove_rear() == 20  # The rear element should be removed
    assert list(deque.items) == [10]


def test_is_empty_on_empty_deque() -> None:
    """
    Test case 5: Test checking if an empty deque is empty.
    """
    deque = Deque[int]()
    assert deque.is_empty() is True


def test_is_empty_on_non_empty_deque() -> None:
    """
    Test case 6: Test checking if a non-empty deque is empty.
    """
    deque = Deque[int]()
    deque.add_front(10)
    assert deque.is_empty() is False


def test_size_of_empty_deque() -> None:
    """
    Test case 7: Test the size of an empty deque.
    """
    deque = Deque[int]()
    assert deque.size() == 0


def test_size_of_non_empty_deque() -> None:
    """
    Test case 8: Test the size of a non-empty deque.
    """
    deque = Deque[int]()
    deque.add_front(10)
    deque.add_rear(20)
    assert deque.size() == 2


def test_remove_front_from_empty_deque() -> None:
    """
    Test case 9: Test removing an element from the front of an empty deque.
    """
    deque = Deque[int]()
    with pytest.raises(IndexError, match="Remove from an empty deque"):
        deque.remove_front()


def test_remove_rear_from_empty_deque() -> None:
    """
    Test case 10: Test removing an element from the rear of an empty deque.
    """
    deque = Deque[int]()
    with pytest.raises(IndexError, match="Remove from an empty deque"):
        deque.remove_rear()


def test_mixed_operations() -> None:
    """
    Test case 11: Test a mix of operations on the deque.
    """
    deque = Deque[int]()
    deque.add_front(10)
    deque.add_rear(20)
    deque.add_front(5)
    deque.add_rear(25)
    assert list(deque.items) == [5, 10, 20, 25]
    assert deque.remove_front() == 5
    assert deque.remove_rear() == 25
    assert list(deque.items) == [10, 20]
    assert deque.size() == 2
    assert deque.is_empty() is False


def test_add_and_remove_all_elements() -> None:
    """
    Test case 12: Test adding and removing all elements from the deque.
    """
    deque = Deque[int]()
    deque.add_front(10)
    deque.add_rear(20)
    deque.add_front(5)
    deque.add_rear(25)
    assert deque.remove_front() == 5
    assert deque.remove_front() == 10
    assert deque.remove_rear() == 25
    assert deque.remove_rear() == 20
    assert deque.is_empty() is True


def test_single_element_operations() -> None:
    """
    Test case 13: Test adding and removing a single element.
    """
    deque = Deque[int]()
    deque.add_front(10)
    assert deque.size() == 1
    assert deque.remove_front() == 10
    assert deque.is_empty() is True

    deque.add_rear(20)
    assert deque.size() == 1
    assert deque.remove_rear() == 20
    assert deque.is_empty() is True


def test_large_deque_operations() -> None:
    """
    Test case 14: Test adding and removing a large number of elements.
    """
    deque = Deque[int]()
    for i in range(1000):  # Add 1000 elements to the rear
        deque.add_rear(i)
    assert deque.size() == 1000

    for i in range(500):  # Remove 500 elements from the front
        assert deque.remove_front() == i
    assert deque.size() == 500

    for i in range(999, 499, -1):  # Remove 500 elements from the rear
        assert deque.remove_rear() == i
    assert deque.is_empty() is True


def test_custom_type_operations() -> None:

    """
    Test case 15: Test deque operations with a custom type.
    """
    class CustomType:
        def __init__(self, value: int) -> None:
            self.value = value

        def __eq__(self, other: object) -> bool:
            if isinstance(other, CustomType):
                return self.value == other.value
            return False

    deque = Deque[CustomType]()
    obj1 = CustomType(1)
    obj2 = CustomType(2)
    obj3 = CustomType(3)

    deque.add_front(obj1)
    deque.add_rear(obj2)
    deque.add_front(obj3)

    assert deque.size() == 3
    assert deque.remove_front() == obj3
    assert deque.remove_rear() == obj2
    assert deque.remove_front() == obj1
    assert deque.is_empty() is True


def test_empty_deque_boundary() -> None:
    """
    Test case 16: Test operations on an empty deque.
    """
    deque = Deque[int]()
    assert deque.is_empty() is True
    assert deque.size() == 0

    with pytest.raises(IndexError, match="Remove from an empty deque"):
        deque.remove_front()

    with pytest.raises(IndexError, match="Remove from an empty deque"):
        deque.remove_rear()
