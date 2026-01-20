"""
Assert dictionary contains expected key-value pairs.
"""

from typing import Any


def assert_dict_contains(
    actual_dict: dict[Any, Any],
    expected_subset: dict[Any, Any],
) -> None:
    """
    Assert that a dictionary contains all key-value pairs from another dict.

    Parameters
    ----------
    actual_dict : dict[Any, Any]
        Dictionary to check.
    expected_subset : dict[Any, Any]
        Expected subset of key-value pairs.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are not dictionaries.
    AssertionError
        If expected keys are missing or values don't match.

    Examples
    --------
    >>> assert_dict_contains({'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 2})
    >>> assert_dict_contains({'x': 'y'}, {'x': 'y'})

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(actual_dict, dict):
        raise TypeError(f"actual_dict must be a dict, got {type(actual_dict).__name__}")
    if not isinstance(expected_subset, dict):
        raise TypeError(
            f"expected_subset must be a dict, got {type(expected_subset).__name__}"
        )

    for key, expected_value in expected_subset.items():
        if key not in actual_dict:
            raise AssertionError(f"Key '{key}' not found in actual dictionary")

        actual_value = actual_dict[key]
        if actual_value != expected_value:
            raise AssertionError(
                f"Value mismatch for key '{key}': "
                f"actual={actual_value}, expected={expected_value}"
            )


__all__ = ["assert_dict_contains"]
