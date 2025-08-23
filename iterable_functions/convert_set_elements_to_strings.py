from typing import Any


def convert_set_elements_to_strings(input_set: set[Any]) -> set[str]:
    """
    Convert all elements in the set to strings.

    Parameters
    ----------
    input_set : set
        The set of elements to be converted to strings.

    Returns
    -------
    set
        A set with all elements converted to strings.

    Raises
    ------
    TypeError
        If input_set is not a set or contains elements that cannot be converted to strings.
    """
    if not isinstance(input_set, set):
        raise TypeError("input_set must be a set")

    try:
        return {str(element) for element in input_set}
    except Exception as e:
        raise TypeError(
            f"An element in the set cannot be converted to a string: {e}")


__all__ = ['convert_set_elements_to_strings']
