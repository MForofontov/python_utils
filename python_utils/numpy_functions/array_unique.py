import numpy as np


def array_unique(arr: np.ndarray) -> np.ndarray:
    """
    Return the sorted unique elements of a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Sorted unique elements of the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_unique(np.array([1, 2, 2, 3]))
    array([1, 2, 3])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.unique(arr)


__all__ = ["array_unique"]
