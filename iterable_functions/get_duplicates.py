from collections import Counter
from typing import Any


def get_duplicates(input_list: list[Any]) -> list[Any]:
    """
    Identify duplicate elements in a list.

    Parameters
    ----------
    input_list : list
        The list to check for duplicate elements.

    Returns
    -------
    list
        A list containing the duplicate elements found in the input list.

    Raises
    ------
    TypeError
        If input_list is not a list.
    """
    if not isinstance(input_list, list):
        raise TypeError("input_list must be a list")

    element_counts = Counter(input_list)
    duplicates = [element for element,
                  count in element_counts.items() if count > 1]
    return duplicates


__all__ = ['get_duplicates']
