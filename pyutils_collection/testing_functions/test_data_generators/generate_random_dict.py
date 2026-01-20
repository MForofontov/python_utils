"""
Generate random dictionary for testing.
"""

from typing import Any

from .generate_random_float import generate_random_float
from .generate_random_int import generate_random_int
from .generate_random_string import generate_random_string


def generate_random_dict(
    num_keys: int = 5,
    key_prefix: str = "key",
    value_type: str = "int",
) -> dict[str, Any]:
    """
    Generate a random dictionary.

    Parameters
    ----------
    num_keys : int, optional
        Number of keys in the dictionary (by default 5).
    key_prefix : str, optional
        Prefix for keys (by default "key").
    value_type : str, optional
        Type of values: 'int', 'float', 'str' (by default 'int').

    Returns
    -------
    dict[str, Any]
        Random dictionary.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If num_keys is negative or value_type is invalid.

    Examples
    --------
    >>> result = generate_random_dict(3, "test")
    >>> len(result)
    3
    >>> all(k.startswith("test") for k in result.keys())
    True

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(num_keys, int):
        raise TypeError(f"num_keys must be an integer, got {type(num_keys).__name__}")
    if not isinstance(key_prefix, str):
        raise TypeError(f"key_prefix must be a string, got {type(key_prefix).__name__}")
    if not isinstance(value_type, str):
        raise TypeError(f"value_type must be a string, got {type(value_type).__name__}")

    if num_keys < 0:
        raise ValueError(f"num_keys must be non-negative, got {num_keys}")
    if value_type not in ("int", "float", "str"):
        raise ValueError(
            f"value_type must be 'int', 'float', or 'str', got {value_type}"
        )

    result: dict[str, Any] = {}
    for i in range(num_keys):
        key = f"{key_prefix}_{i}"
        if value_type == "int":
            result[key] = generate_random_int()
        elif value_type == "float":
            result[key] = generate_random_float()
        else:  # str
            result[key] = generate_random_string()

    return result


__all__ = ["generate_random_dict"]
