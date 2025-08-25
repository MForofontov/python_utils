"""Calculate the mode of a list of values."""

from typing import Union, Any
from collections import Counter


def mode(values: list[Any]) -> Union[Any, list[Any]]:
    """
    Calculate the mode (most frequently occurring value) of a list.

    Parameters
    ----------
    values : list[Any]
        List of values of any comparable type.

    Returns
    -------
    Any | list[Any]
        The most frequently occurring value(s). Returns a single value if there 
        is one mode, or a list of values if there are multiple modes with the 
        same highest frequency.

    Raises
    ------
    TypeError
        If values is not a list.
    ValueError
        If the list is empty.

    Examples
    --------
    >>> mode([1, 2, 2, 3, 4])
    2
    >>> mode([1, 1, 2, 2, 3])
    [1, 2]
    >>> mode(['a', 'b', 'b', 'c'])
    'b'
    >>> mode([1, 2, 3])
    [1, 2, 3]
    """
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    # Count frequencies
    counter = Counter(values)
    max_count = max(counter.values())
    
    # Find all values with maximum frequency
    modes = [value for value, count in counter.items() if count == max_count]
    
    # Return single value if only one mode, otherwise return list
    if len(modes) == 1:
        return modes[0]
    else:
        # Try to sort if all modes are of comparable types
        try:
            return sorted(modes)
        except TypeError:
            # If sorting fails (mixed incomparable types), return unsorted
            return modes


__all__ = ['mode']
