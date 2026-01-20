"""JSON merging utilities."""

import copy
from typing import Any


def json_merge(a: Any, b: Any, deep: bool = True) -> Any:
    """
    Merge two JSON-serializable objects (dicts/lists/primitives).

    Parameters
    ----------
    a : Any
        First object to merge.
    b : Any
        Second object to merge (takes precedence).
    deep : bool, optional
        If True, merge recursively for nested dicts/lists (default: True).

    Returns
    -------
    Any
        Merged object. If both are dicts, merge keys (b overrides a).
        If both are lists, concatenate. Otherwise, return b if not None.

    Raises
    ------
    TypeError
        If 'deep' is not a boolean.

    Examples
    --------
    >>> json_merge({'a': 1}, {'b': 2})
    {'a': 1, 'b': 2}
    >>> json_merge([1, 2], [3, 4])
    [1, 2, 3, 4]
    """
    # Input validation for 'deep' parameter
    if not isinstance(deep, bool):
        raise TypeError(f"deep must be a bool, got {type(deep).__name__}")

    if isinstance(a, dict) and isinstance(b, dict):
        result = copy.deepcopy(a)
        for k, v in b.items():
            if k in result and deep:
                result[k] = json_merge(result[k], v, deep=deep)
            else:
                result[k] = copy.deepcopy(v)
        return result
    elif isinstance(a, list) and isinstance(b, list):
        return copy.deepcopy(a) + copy.deepcopy(b)
    else:
        return copy.deepcopy(b) if b is not None else copy.deepcopy(a)
