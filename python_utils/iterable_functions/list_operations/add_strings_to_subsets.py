"""Add strings to subsets using clustering algorithm."""


def add_strings_to_subsets(my_list: list[set[str]], my_strings: list[str]) -> bool:
    """
    Clustering algorithm that finds a string in a list of strings in
    a list of sets and adds the whole list to the set if any string of
    that list is inside the set.

    Parameters
    ----------
    my_list : list of sets
        The list of sets to add strings to.
    my_strings : list of str
        The list of strings to add to the sets.

    Returns
    -------
    bool
        True if any string was added to a set, False otherwise.

    Raises
    ------
    TypeError
        If my_list is not a list of sets or my_strings is not a list of strings.
    """
    if not isinstance(my_list, list) or not all(
        isinstance(sublist, set) for sublist in my_list
    ):
        raise TypeError("my_list must be a list of sets")
    if not isinstance(my_strings, list) or not all(
        isinstance(s, str) for s in my_strings
    ):
        raise TypeError("my_strings must be a list of strings")

    found = False
    for my_string in my_strings:
        if found:
            break
        for sublist in my_list:
            if my_string in sublist:
                sublist.update(my_strings)
                found = True
                break
    return found


__all__ = ["add_strings_to_subsets"]
