from typing import TypeVar


KT = TypeVar("KT", str, int)
VT = TypeVar("VT")


def identify_value_in_dict_get_key(
    target_value: VT, dictionary: dict[KT, VT]
) -> KT | None:
    """Identify the key in the dictionary where the target value is present.

    Parameters
    ----------
    target_value : VT
        The value to find.
    dictionary : dict[KT, VT]
        The dictionary where to find the value.

    Returns
    -------
    KT or None
        The key of the entry where the value is present, or None if not found.

    Raises
    ------
    TypeError
        If dictionary is not a dictionary.
    """
    if not isinstance(dictionary, dict):
        raise TypeError("dictionary must be a dictionary")

    for key, value in dictionary.items():
        if target_value == value:
            return key
    return None


__all__ = ["identify_value_in_dict_get_key"]
