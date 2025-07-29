from typing import Any


def is_nested_list_empty(input_list: list[Any]) -> bool:
    """
    Check if a nested list is empty.

    Parameters
    ----------
    input_list : list
        Input list to verify

    Returns
    -------
    bool
        True if the list is empty or contains only empty nested lists, False otherwise.

    Raises
    ------
    TypeError
        If input_list is not a list.
    """
    if not isinstance(input_list, list):
        raise TypeError("input_list must be a list")

    return (
        all(
            is_nested_list_empty(item) if isinstance(item, list) else False
            for item in input_list
        )
        if input_list
        else True
    )

__all__ = ['is_nested_list_empty']
