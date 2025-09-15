"""
Value range validation utility for numeric and comparable values.

This module provides comprehensive value range validation with support for
minimum/maximum bounds, exclusive bounds, and custom comparison logic.
"""

from typing import TypeVar

T = TypeVar("T")


def validate_range(
    value: T,
    min_value: T | None = None,
    max_value: T | None = None,
    min_inclusive: bool = True,
    max_inclusive: bool = True,
    param_name: str = "value",
) -> None:
    """
    Validate that a value falls within the specified range.

    Supports both inclusive and exclusive bounds for minimum and maximum values.
    Works with any comparable types including numbers, strings, and dates.

    Parameters
    ----------
    value : T
        The value to validate.
    min_value : T | None, optional
        Minimum allowed value (by default None for no minimum).
    max_value : T | None, optional
        Maximum allowed value (by default None for no maximum).
    min_inclusive : bool, optional
        Whether minimum bound is inclusive (by default True).
    max_inclusive : bool, optional
        Whether maximum bound is inclusive (by default True).
    param_name : str, optional
        Name of the parameter being validated for error messages (by default "value").

    Returns
    -------
    None
        This function returns None if validation passes.

    Raises
    ------
    ValueError
        If the value is outside the specified range.
    TypeError
        If value types are incompatible for comparison.

    Examples
    --------
    >>> validate_range(5, min_value=0, max_value=10)  # Passes
    >>> validate_range(5.5, min_value=0.0, max_value=10.0)  # Passes
    >>> validate_range("hello", min_value="a", max_value="z")  # Passes
    >>> validate_range(-1, min_value=0)  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: value must be >= 0, got -1

    >>> validate_range(10, min_value=0, max_value=10, max_inclusive=False)  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: value must be < 10, got 10

    >>> from datetime import date
    >>> validate_range(date(2023, 6, 15), min_value=date(2023, 1, 1), max_value=date(2023, 12, 31))  # Passes

    Notes
    -----
    This function provides comprehensive range validation including:
    - Numeric ranges (int, float, Decimal, etc.)
    - String lexicographic ranges
    - Date and datetime ranges
    - Custom comparable objects
    - Inclusive and exclusive bounds
    - Detailed error messages

    The function uses Python's comparison operators, so it works with any
    objects that implement __lt__, __le__, __gt__, __ge__ methods.

    Complexity
    ----------
    Time: O(1) - constant time comparisons
    Space: O(1)
    """
    # Validate input types
    if not isinstance(min_inclusive, bool):
        raise TypeError(
            f"min_inclusive must be bool, got {type(min_inclusive).__name__}"
        )
    if not isinstance(max_inclusive, bool):
        raise TypeError(
            f"max_inclusive must be bool, got {type(max_inclusive).__name__}"
        )
    if not isinstance(param_name, str):
        raise TypeError(f"param_name must be str, got {type(param_name).__name__}")

    # Check minimum bound
    if min_value is not None:
        try:
            if min_inclusive:
                if value < min_value:
                    raise ValueError(
                        f"{param_name} must be >= {min_value}, got {value}"
                    )
            else:
                if value <= min_value:
                    raise ValueError(f"{param_name} must be > {min_value}, got {value}")
        except TypeError as e:
            raise TypeError(
                f"Cannot compare {param_name} of type {type(value).__name__} "
                f"with min_value of type {type(min_value).__name__}"
            ) from e

    # Check maximum bound
    if max_value is not None:
        try:
            if max_inclusive:
                if value > max_value:
                    raise ValueError(
                        f"{param_name} must be <= {max_value}, got {value}"
                    )
            else:
                if value >= max_value:
                    raise ValueError(f"{param_name} must be < {max_value}, got {value}")
        except TypeError as e:
            raise TypeError(
                f"Cannot compare {param_name} of type {type(value).__name__} "
                f"with max_value of type {type(max_value).__name__}"
            ) from e

    # Check that min_value <= max_value if both are provided
    if min_value is not None and max_value is not None:
        try:
            if min_value > max_value:
                raise ValueError(
                    f"min_value ({min_value}) cannot be greater than max_value ({max_value})"
                )
            if min_value == max_value and not (min_inclusive and max_inclusive):
                raise ValueError(
                    f"min_value and max_value are equal ({min_value}), "
                    "but at least one bound is exclusive"
                )
        except TypeError as e:
            raise TypeError(
                f"Cannot compare min_value of type {type(min_value).__name__} "
                f"with max_value of type {type(max_value).__name__}"
            ) from e


__all__ = ["validate_range"]
