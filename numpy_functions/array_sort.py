import numpy as np


def array_sort(arr: np.ndarray) -> np.ndarray:
    """
    Return a sorted copy of a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Sorted array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_sort(np.array([3, 1, 2]))
    array([1, 2, 3])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.sort(arr)


__all__ = ["array_sort"]
