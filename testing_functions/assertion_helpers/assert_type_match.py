"""
Assert value is of expected type.
"""

from typing import Any


def assert_type_match(
    value: Any,
    expected_type: type[Any],
) -> None:
    """
    Assert that a value is of the expected type.

    Parameters
    ----------
    value : Any
        Value to check.
    expected_type : Type[Any]
        Expected type.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If expected_type is not a type.
    AssertionError
        If value is not of expected type.

    Examples
    --------
    >>> assert_type_match(5, int)
    >>> assert_type_match("hello", str)

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(expected_type, type):
        raise TypeError(
            f"expected_type must be a type, got {type(expected_type).__name__}"
        )

    if not isinstance(value, expected_type):
        raise AssertionError(
            f"Type mismatch: expected {expected_type.__name__}, "
            f"got {type(value).__name__}"
        )


__all__ = ["assert_type_match"]
