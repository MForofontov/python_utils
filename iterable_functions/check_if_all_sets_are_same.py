from typing import Any


def check_if_all_sets_are_same(sets_list: list[set[Any]]) -> bool:
    """
    Checks if all sets within a list are identical.

    Parameters
    ----------
    sets_list : list
        A list of sets to be checked for identity.

    Returns
    -------
    bool
        True if all sets in the list are identical, False otherwise.

    Raises
    ------
    TypeError
        If sets_list is not a list of sets.
    """
    if not isinstance(sets_list, list) or not all(
        isinstance(s, set) for s in sets_list
    ):
        raise TypeError("sets_list must be a list of sets")

    if len(sets_list) <= 1:
        return True

    reference_set = sets_list[0]

    for s in sets_list[1:]:
        if s != reference_set:
            return False

    return True

__all__ = ['check_if_all_sets_are_same']
