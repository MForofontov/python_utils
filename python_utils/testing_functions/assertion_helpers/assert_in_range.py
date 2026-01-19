"""
Assert value is within a specified range.
"""


def assert_in_range(
    value: float,
    min_value: float,
    max_value: float,
) -> None:
    """
    Assert that a value is within a specified range.

    Parameters
    ----------
    value : float
        Value to check.
    min_value : float
        Minimum value (inclusive).
    max_value : float
        Maximum value (inclusive).

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If min_value > max_value.
    AssertionError
        If value is outside the range.

    Examples
    --------
    >>> assert_in_range(5, 1, 10)
    >>> assert_in_range(1, 1, 1)

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"value must be a number, got {type(value).__name__}")
    if not isinstance(min_value, (int, float)):
        raise TypeError(f"min_value must be a number, got {type(min_value).__name__}")
    if not isinstance(max_value, (int, float)):
        raise TypeError(f"max_value must be a number, got {type(max_value).__name__}")

    if min_value > max_value:
        raise ValueError(f"min_value ({min_value}) must be <= max_value ({max_value})")

    if not (min_value <= value <= max_value):
        raise AssertionError(
            f"Value {value} is not in range [{min_value}, {max_value}]"
        )


__all__ = ["assert_in_range"]
