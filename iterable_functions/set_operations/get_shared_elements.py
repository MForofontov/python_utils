from collections import Counter
from typing import TypeVar

T = TypeVar("T")


def get_shared_elements(dict_: dict[str, list[T]]) -> list[T]:
    """
    Identify elements that appear in at least two lists within a dictionary.

    Parameters
    ----------
    dict_ : dict[str, list[T]]
        A dictionary where the values are lists of elements.

    Returns
    -------
    list[T]
        A list containing elements that appear in at least two lists within the dictionary.

    Raises
    ------
    TypeError
        If dict_ is not a dictionary or if any value in dict_ is not a list.
    ValueError
        If any list contains unhashable elements.
    """
    if not isinstance(dict_, dict):
        raise TypeError("dict_ must be a dictionary")
    if not all(isinstance(value, list) for value in dict_.values()):
        raise TypeError("All values in dict_ must be lists")

    all_elements = []
    for sublist in dict_.values():
        try:
            all_elements.extend(sublist)
        except TypeError as exc:
            raise TypeError(
                f"Sublist contains unhashable elements: {exc}"
            ) from exc

    element_counts = Counter(all_elements)
    shared_elements = [elem for elem, count in element_counts.items() if count >= 2]
    return shared_elements


__all__ = ["get_shared_elements"]
