import pytest
from data_types.LinkedList import LinkedList

def test_append() -> None:
    """
    Test appending elements to the linked list.
    """
    # Test case 1: Append elements
    linked_list = LinkedList[int]()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.size() == 3
    assert linked_list.search(1) is True
    assert linked_list.search(2) is True
    assert linked_list.search(3) is True

def test_prepend() -> None:
    """
    Test prepending elements to the linked list.
    """
    # Test case 2: Prepend elements
    linked_list = LinkedList[int]()
    linked_list.prepend(1)
    linked_list.prepend(2)
    linked_list.prepend(3)
    assert linked_list.size() == 3
    assert linked_list.search(1) is True
    assert linked_list.search(2) is True
    assert linked_list.search(3) is True

def test_delete() -> None:
    """
    Test deleting elements from the linked list.
    """
    # Test case 3: Delete elements
    linked_list = LinkedList[int]()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.delete(2)
    assert linked_list.size() == 2
    assert linked_list.search(2) is False
    assert linked_list.search(1) is True
    assert linked_list.search(3) is True

def test_delete_head() -> None:
    """
    Test deleting the head element from the linked list.
    """
    # Test case 4: Delete head
    linked_list = LinkedList[int]()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    assert linked_list.size() == 1
    assert linked_list.search(1) is False
    assert linked_list.search(2) is True

def test_search() -> None:
    """
    Test searching for elements in the linked list.
    """
    # Test case 5: Search elements
    linked_list = LinkedList[int]()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.search(1) is True
    assert linked_list.search(2) is True
    assert linked_list.search(3) is True
    assert linked_list.search(4) is False

def test_size() -> None:
    """
    Test getting the size of the linked list.
    """
    # Test case 6: Size of the list
    linked_list = LinkedList[int]()
    assert linked_list.size() == 0
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.size() == 2
    linked_list.delete(1)
    assert linked_list.size() == 1

def test_custom_object_nodes() -> None:
    """
    Test the linked list with custom object nodes.
    """
    # Test case 7: Custom object nodes
    class CustomObject:
        def __init__(self, value: int) -> None:
            self.value = value

        def __eq__(self, other: object) -> bool:
            if isinstance(other, CustomObject):
                return self.value == other.value
            return False

    linked_list = LinkedList[CustomObject]()
    obj1 = CustomObject(1)
    obj2 = CustomObject(2)
    obj3 = CustomObject(3)
    linked_list.append(obj1)
    linked_list.append(obj2)
    linked_list.append(obj3)
    assert linked_list.search(obj2) is True
    linked_list.delete(obj2)
    assert linked_list.search(obj2) is False

def test_single_node_operations() -> None:
    """
    Test adding and deleting elements in a single-node list.
    """
    # Test case 8: Single-node list
    linked_list = LinkedList[int]()
    linked_list.append(1)
    assert linked_list.size() == 1
    assert linked_list.search(1) is True
    linked_list.delete(1)
    assert linked_list.size() == 0
    assert linked_list.search(1) is False

def test_large_linked_list() -> None:
    """
    Test operations on a very large linked list.
    """
    # Test case 9: Large linked list
    linked_list = LinkedList[int]()
    for i in range(10000):
        linked_list.append(i)
    assert linked_list.size() == 10000
    assert linked_list.search(9999) is True
    linked_list.delete(9999)
    assert linked_list.size() == 9999
    assert linked_list.search(9999) is False

def test_order_of_elements() -> None:
    """
    Test the order of elements in the linked list after multiple operations.
    """
    # Test case 10: Order verification
    linked_list = LinkedList[int]()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.delete(2)
    linked_list.prepend(0)
    current = linked_list.head
    elements = []
    while current:
        elements.append(current.data)
        current = current.next
    assert elements == [0, 1, 3]

def test_iterative_access() -> None:
    """
    Test iteration over the linked list.
    """
    # Test case 11: Iterative access
    linked_list = LinkedList[int]()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    elements = [node.data for node in linked_list]
    assert elements == [1, 2, 3]

def test_delete_nonexistent_element() -> None:
    """
    Test deleting a nonexistent element from the linked list.
    """
    # Test case 12: Delete nonexistent element
    linked_list = LinkedList[int]()
    linked_list.append(1)
    linked_list.append(2)
    with pytest.raises(ValueError, match="Data 3 not found in the list"):
        linked_list.delete(3)

def test_empty_list_operations() -> None:
    """
    Test operations on an empty linked list.
    """
    # Test case 13: Empty list operations
    linked_list = LinkedList[int]()
    assert linked_list.size() == 0
    assert linked_list.search(1) is False
    with pytest.raises(ValueError, match="Data 1 not found in the list"):
        linked_list.delete(1)