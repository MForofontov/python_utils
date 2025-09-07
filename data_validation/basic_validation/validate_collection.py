"""
Collection validation utility for lists, sets, dictionaries, and other iterables.

This module provides comprehensive validation for collection types including
length validation, emptiness checks, and element type validation.
"""

from typing import Any, TypeVar, Union
from collections.abc import Iterable, Sized

T = TypeVar("T")


def validate_collection(
    collection: Any,
    expected_type: type,
    min_length: int | None = None,
    max_length: int | None = None,
    allow_empty: bool = True,
    element_type: type | tuple[type, ...] | None = None,
    param_name: str = "collection",
) -> None:
    """
    Validate collection type, length, and optionally element types.

    Provides comprehensive validation for any collection type including lists,
    tuples, sets, dictionaries, and custom iterable objects.

    Parameters
    ----------
    collection : Any
        The collection to validate.
    expected_type : type
        Expected collection type (list, tuple, set, dict, etc.).
    min_length : int | None, optional
        Minimum allowed length (by default None for no minimum).
    max_length : int | None, optional
        Maximum allowed length (by default None for no maximum).
    allow_empty : bool, optional
        Whether to allow empty collections (by default True).
    element_type : type | tuple[type, ...] | None, optional
        Expected type(s) for collection elements (by default None for no checking).
    param_name : str, optional
        Name of the parameter being validated for error messages (by default "collection").

    Returns
    -------
    None
        This function returns None if validation passes.

    Raises
    ------
    TypeError
        If collection is not of expected type or elements have wrong type.
    ValueError
        If collection length is outside specified bounds or empty when not allowed.

    Examples
    --------
    >>> validate_collection([1, 2, 3], list)  # Passes
    >>> validate_collection([1, 2, 3], list, min_length=2, max_length=5)  # Passes
    >>> validate_collection([1, 2, 3], list, element_type=int)  # Passes
    >>> validate_collection([], list, allow_empty=False)  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: collection cannot be empty

    >>> validate_collection([1, "2", 3], list, element_type=int)  # Raises TypeError
    Traceback (most recent call last):
        ...
    TypeError: collection element at index 1 must be int, got str

    >>> validate_collection({"a": 1, "b": 2}, dict, min_length=1, max_length=3)  # Passes
    >>> validate_collection({1, 2, 3, 4, 5}, set, max_length=3)  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: collection length (5) exceeds maximum allowed length (3)

    Notes
    -----
    This function provides comprehensive collection validation including:
    - Type checking for any collection type
    - Length bounds validation
    - Empty collection handling
    - Element type validation for homogeneous collections
    - Support for union element types
    - Detailed error messages with specific indices for element errors

    Element type validation works by iterating through the collection and
    checking each element. For dictionaries, it validates values only.

    Complexity
    ----------
    Time: O(1) for type/length checks, O(n) for element type validation
    Space: O(1)
    """
    # Validate input parameters
    if not isinstance(expected_type, type):
        raise TypeError("expected_type must be a type")
    if not isinstance(allow_empty, bool):
        raise TypeError(f"allow_empty must be bool, got {type(allow_empty).__name__}")
    if not isinstance(param_name, str):
        raise TypeError(f"param_name must be str, got {type(param_name).__name__}")

    if min_length is not None:
        if not isinstance(min_length, int):
            raise TypeError(f"min_length must be int or None, got {type(min_length).__name__}")
        if min_length < 0:
            raise ValueError(f"min_length must be non-negative, got {min_length}")

    if max_length is not None:
        if not isinstance(max_length, int):
            raise TypeError(f"max_length must be int or None, got {type(max_length).__name__}")
        if max_length < 0:
            raise ValueError(f"max_length must be non-negative, got {max_length}")

    if min_length is not None and max_length is not None and min_length > max_length:
        raise ValueError(f"min_length ({min_length}) cannot be greater than max_length ({max_length})")

    # Validate collection type
    if not isinstance(collection, expected_type):
        raise TypeError(f"{param_name} must be {expected_type.__name__}, got {type(collection).__name__}")

    # Validate that collection is sized (has length)
    if not isinstance(collection, Sized):
        raise TypeError(f"{param_name} must be a sized collection")

    # Get collection length
    length = len(collection)

    # Validate emptiness
    if not allow_empty and length == 0:
        raise ValueError(f"{param_name} cannot be empty")

    # Validate minimum length
    if min_length is not None and length < min_length:
        raise ValueError(f"{param_name} length ({length}) is below minimum allowed length ({min_length})")

    # Validate maximum length
    if max_length is not None and length > max_length:
        raise ValueError(f"{param_name} length ({length}) exceeds maximum allowed length ({max_length})")

    # Validate element types if specified
    if element_type is not None and length > 0:
        # Make collection iterable for element checking
        if not isinstance(collection, Iterable):
            raise TypeError(f"{param_name} must be iterable for element type validation")

        # For dictionaries, validate values
        if isinstance(collection, dict):
            for key, value in collection.items():
                if isinstance(element_type, tuple):
                    if not any(isinstance(value, t) for t in element_type):
                        type_names = " | ".join(t.__name__ for t in element_type)
                        raise TypeError(f"{param_name} value for key '{key}' must be {type_names}, "
                                      f"got {type(value).__name__}")
                else:
                    if not isinstance(value, element_type):
                        raise TypeError(f"{param_name} value for key '{key}' must be {element_type.__name__}, "
                                      f"got {type(value).__name__}")
        else:
            # For other iterables, validate each element
            for index, element in enumerate(collection):
                if isinstance(element_type, tuple):
                    if not any(isinstance(element, t) for t in element_type):
                        type_names = " | ".join(t.__name__ for t in element_type)
                        raise TypeError(f"{param_name} element at index {index} must be {type_names}, "
                                      f"got {type(element).__name__}")
                else:
                    if not isinstance(element, element_type):
                        raise TypeError(f"{param_name} element at index {index} must be {element_type.__name__}, "
                                      f"got {type(element).__name__}")


__all__ = ['validate_collection']
