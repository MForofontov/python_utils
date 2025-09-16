from collections import Counter
from typing import TypeVar

T = TypeVar("T")


def check_if_all_elements_are_duplicates(input_list: list[T]) -> bool:
    """
    Check if all elements in the list are duplicates.

    Parameters
    ----------
    input_list : list[T]
        The list to check for duplicate elements.

    Returns
    -------
    bool
        True if every element in the list occurs more than once, False otherwise.
        Returns False if the list is empty.

    Raises
    ------
    TypeError
        If input_list is not a list.
    """
    if not isinstance(input_list, list):
        raise TypeError("input_list must be a list")

    element_counts = Counter(
        tuple(element) if isinstance(element, list) else element
        for element in input_list
    )

    return (
        all(count > 1 for count in element_counts.values()) if element_counts else False
    )


__all__ = ["check_if_all_elements_are_duplicates"]
