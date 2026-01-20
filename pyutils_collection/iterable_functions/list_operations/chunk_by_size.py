"""Split list into chunks of specified size."""

from typing import TypeVar

T = TypeVar("T")


def chunk_by_size(items: list[T], chunk_size: int) -> list[list[T]]:
    """
    Split a list into chunks of specified size.

    Parameters
    ----------
    items : list[T]
        The list to be chunked.
    chunk_size : int
        The size of each chunk.

    Returns
    -------
    list[list[T]]
        List of chunks, where each chunk is a list of items.

    Raises
    ------
    TypeError
        If items is not a list or chunk_size is not an integer.
    ValueError
        If chunk_size is less than or equal to 0.

    Examples
    --------
    >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> chunk_by_size(numbers, 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

    >>> letters = ['a', 'b', 'c', 'd']
    >>> chunk_by_size(letters, 2)
    [['a', 'b'], ['c', 'd']]

    >>> empty_list = []
    >>> chunk_by_size(empty_list, 5)
    []

    Notes
    -----
    The last chunk may contain fewer items if the total number of items
    is not evenly divisible by chunk_size.

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    # Input validation
    if not isinstance(items, list):
        raise TypeError(f"items must be a list, got {type(items).__name__}")

    if not isinstance(chunk_size, int):
        raise TypeError(
            f"chunk_size must be an integer, got {type(chunk_size).__name__}"
        )

    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")

    # Handle empty list
    if not items:
        return []

    # Create chunks
    chunks = []
    for i in range(0, len(items), chunk_size):
        chunks.append(items[i : i + chunk_size])

    return chunks


__all__ = ["chunk_by_size"]
