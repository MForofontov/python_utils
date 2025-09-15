from typing import Any


def identify_dict_structure(list_of_dicts: list[dict[str, Any]]) -> dict[str, None]:
    """
    Identify all keys present in a list of dictionaries, including nested dictionaries.

    Parameters
    ----------
    list_of_dicts : list of dict
        The list of dictionaries to analyze.

    Returns
    -------
    dict
        A dictionary where keys are all unique keys present in the list of dictionaries, including nested dictionaries, and values are None.

    Raises
    ------
    TypeError
        If list_of_dicts is not a list of dictionaries.
    """
    if not isinstance(list_of_dicts, list):
        raise TypeError("list_of_dicts must be a list")
    if not all(isinstance(d, dict) for d in list_of_dicts):
        raise TypeError("all elements in list_of_dicts must be dictionaries")

    keys: dict[str, None] = {}

    def extract_keys(d: dict[str, Any], parent_key: str = "") -> None:
        for key, value in d.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            keys[full_key] = None
            if isinstance(value, dict):
                extract_keys(value, full_key)
            elif isinstance(value, list) or isinstance(value, tuple):
                for item in value:
                    if isinstance(item, dict):
                        extract_keys(item, full_key)

    for dictionary in list_of_dicts:
        extract_keys(dictionary)

    return keys


__all__ = ["identify_dict_structure"]
