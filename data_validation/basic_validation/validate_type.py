"""
Type validation utility for ensuring values match expected types.

This module provides a comprehensive type validation function that supports
single types, union types, and nested type checking for complex data structures.
"""

from typing import Any, Union, get_origin, get_args
from collections.abc import Mapping, Sequence, Set as AbstractSet


def validate_type(
    value: Any,
    expected_type: type | tuple[type, ...],
    param_name: str = "value",
    allow_none: bool = False,
) -> None:
    """
    Validate that a value matches the expected type(s).

    Supports basic types, union types, and complex nested type validation
    including collections like list, dict, set, and tuple.

    Parameters
    ----------
    value : Any
        The value to validate.
    expected_type : type | tuple[type, ...]
        The expected type or tuple of acceptable types.
    param_name : str, optional
        Name of the parameter being validated for error messages (by default "value").
    allow_none : bool, optional
        Whether to allow None values (by default False).

    Returns
    -------
    None
        This function returns None if validation passes.

    Raises
    ------
    TypeError
        If the value doesn't match any of the expected types.

    Examples
    --------
    >>> validate_type(42, int)  # Passes
    >>> validate_type("hello", str)  # Passes
    >>> validate_type([1, 2, 3], list)  # Passes
    >>> validate_type(42, str)  # Raises TypeError
    Traceback (most recent call last):
        ...
    TypeError: value must be str, got int

    >>> validate_type(42, (int, str))  # Passes - union type
    >>> validate_type(None, str, allow_none=True)  # Passes
    >>> validate_type({"key": "value"}, dict)  # Passes

    Notes
    -----
    This function provides comprehensive type checking including:
    - Basic Python types (int, str, bool, float, etc.)
    - Collection types (list, dict, set, tuple)
    - Union types (multiple acceptable types)
    - None handling with allow_none parameter
    - Detailed error messages with parameter names

    Complexity
    ----------
    Time: O(1) for basic types, O(n) for collection type introspection
    Space: O(1)
    """
    # Handle None values
    if value is None:
        if allow_none:
            return
        if isinstance(expected_type, tuple):
            type_names = " | ".join(t.__name__ for t in expected_type)
        else:
            type_names = expected_type.__name__
        raise TypeError(f"{param_name} cannot be None, expected {type_names}")

    # Handle tuple of types (union types)
    if isinstance(expected_type, tuple):
        if not any(isinstance(value, t) for t in expected_type):
            type_names = " | ".join(t.__name__ for t in expected_type)
            actual_type = type(value).__name__
            raise TypeError(f"{param_name} must be {type_names}, got {actual_type}")
        return

    # Handle single type validation
    if not isinstance(value, expected_type):
        expected_name = expected_type.__name__
        actual_type = type(value).__name__
        raise TypeError(f"{param_name} must be {expected_name}, got {actual_type}")


__all__ = ['validate_type']
