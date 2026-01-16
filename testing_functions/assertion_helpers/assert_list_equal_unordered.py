"""
Assert two lists contain the same elements, ignoring order.
"""

from typing import Any


def assert_list_equal_unordered(
    actual: list[Any],
    expected: list[Any],
) -> None:
    """
    Assert that two lists contain the same elements, ignoring order.

    Parameters
    ----------
    actual : list[Any]
        Actual list.
    expected : list[Any]
        Expected list.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are not lists.
    AssertionError
        If lists don't contain the same elements.

    Examples
    --------
    >>> assert_list_equal_unordered([1, 2, 3], [3, 2, 1])
    >>> assert_list_equal_unordered(['a', 'b'], ['b', 'a'])

    Complexity
    ----------
    Time: O(n log n), Space: O(n)
    """
    if not isinstance(actual, list):
        raise TypeError(f"actual must be a list, got {type(actual).__name__}")
    if not isinstance(expected, list):
        raise TypeError(f"expected must be a list, got {type(expected).__name__}")

    if len(actual) != len(expected):
        raise AssertionError(
            f"Lists have different lengths: actual={len(actual)}, expected={len(expected)}"
        )

    sorted_actual = sorted(actual, key=str)
    sorted_expected = sorted(expected, key=str)

    if sorted_actual != sorted_expected:
        raise AssertionError(
            f"Lists contain different elements:\nactual={actual}\nexpected={expected}"
        )


__all__ = ["assert_list_equal_unordered"]
