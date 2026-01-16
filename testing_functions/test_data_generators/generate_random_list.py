"""
Generate random list for testing.
"""

from typing import Any

from .generate_random_float import generate_random_float
from .generate_random_int import generate_random_int
from .generate_random_string import generate_random_string


def generate_random_list(
    length: int = 10,
    element_type: str = "int",
    min_value: int | float = 0,
    max_value: int | float = 100,
) -> list[Any]:
    """
    Generate a random list of specified type and length.

    Parameters
    ----------
    length : int, optional
        Length of the list (by default 10).
    element_type : str, optional
        Type of elements: 'int', 'float', 'str' (by default 'int').
    min_value : int | float, optional
        Minimum value for numeric types (by default 0).
    max_value : int | float, optional
        Maximum value for numeric types (by default 100).

    Returns
    -------
    list[Any]
        Random list of specified type.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If length is negative or element_type is invalid.

    Examples
    --------
    >>> result = generate_random_list(5, "int", 1, 10)
    >>> len(result)
    5
    >>> result = generate_random_list(3, "str")
    >>> len(result)
    3

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(length, int):
        raise TypeError(f"length must be an integer, got {type(length).__name__}")
    if not isinstance(element_type, str):
        raise TypeError(
            f"element_type must be a string, got {type(element_type).__name__}"
        )
    if not isinstance(min_value, (int, float)):
        raise TypeError(f"min_value must be a number, got {type(min_value).__name__}")
    if not isinstance(max_value, (int, float)):
        raise TypeError(f"max_value must be a number, got {type(max_value).__name__}")

    if length < 0:
        raise ValueError(f"length must be non-negative, got {length}")
    if element_type not in ("int", "float", "str"):
        raise ValueError(
            f"element_type must be 'int', 'float', or 'str', got {element_type}"
        )

    if element_type == "int":
        return [
            generate_random_int(int(min_value), int(max_value)) for _ in range(length)
        ]
    elif element_type == "float":
        return [
            generate_random_float(float(min_value), float(max_value))
            for _ in range(length)
        ]
    else:  # str
        return [generate_random_string() for _ in range(length)]


__all__ = ["generate_random_list"]
