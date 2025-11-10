from typing import Any


def divide_list_into_n_chunks(list_to_divide: list[Any], n: int) -> list[list[Any]]:
    """
    Divides a list into a specified number of sublists.

    Parameters
    ----------
    list_to_divide : list
        The list to divide into sublists.
    n : int
        The number of sublists to create.

    Returns
    -------
    list
        A list of ``n`` sublists created by dividing the input list. Some
        sublists may be empty when ``n`` is greater than the length of the
        input list.

    Raises
    ------
    TypeError
        If list_to_divide is not a list or n is not an integer.
    ValueError
        If n is less than or equal to 0.

    Examples
    --------
    >>> divide_list_into_n_chunks([1, 2, 3, 4, 5], 2)
    [[1, 2, 3], [4, 5]]
    >>> divide_list_into_n_chunks([1, 2], 5)
    [[1], [2], [], [], []]
    """
    if not isinstance(list_to_divide, list):
        raise TypeError("list_to_divide must be a list")
    if type(n) is not int:
        raise TypeError("n must be an integer")
    if n <= 0:
        raise ValueError("n must be greater than 0")

    sublists = []
    list_length = len(list_to_divide)
    sublist_size, remainder = divmod(list_length, n)

    start_idx = 0
    for i in range(n):
        sublist_length = sublist_size + (1 if i < remainder else 0)
        end_idx = start_idx + sublist_length
        sublists.append(list_to_divide[start_idx:end_idx])
        start_idx = end_idx

    return sublists


__all__ = ["divide_list_into_n_chunks"]
