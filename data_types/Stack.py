from typing import Any, List

class Stack:
    """
    A Stack data structure.

    Attributes
    ----------
    items : List[Any]
        The list to store stack elements.

    Methods
    -------
    push(item)
        Adds an element to the top of the stack.
    pop()
        Removes and returns the top element of the stack.
    peek()
        Returns the top element of the stack without removing it.
    is_empty()
        Checks if the stack is empty.
    size()
        Returns the number of elements in the stack.
    """

    def __init__(self) -> None:
        """
        Initializes an empty stack.
        """
        self.items: List[Any] = []

    def push(self, item: Any) -> None:
        """
        Adds an element to the top of the stack.

        Parameters
        ----------
        item : Any
            The element to add to the stack.
        """
        self.items.append(item)

    def pop(self) -> Any:
        """
        Removes and returns the top element of the stack.

        Returns
        -------
        Any
            The top element of the stack.

        Raises
        ------
        IndexError
            If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self.items.pop()

    def peek(self) -> Any:
        """
        Returns the top element of the stack without removing it.

        Returns
        -------
        Any
            The top element of the stack.

        Raises
        ------
        IndexError
            If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self.items[-1]

    def is_empty(self) -> bool:
        """
        Checks if the stack is empty.

        Returns
        -------
        bool
            True if the stack is empty, False otherwise.
        """
        return len(self.items) == 0

    def size(self) -> int:
        """
        Returns the number of elements in the stack.

        Returns
        -------
        int
            The number of elements in the stack.
        """
        return len(self.items)
