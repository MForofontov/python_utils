import numpy as np


def array_cumsum(arr: np.ndarray) -> np.ndarray:
    """
    Compute the cumulative sum of elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Array of the cumulative sum of the input array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_cumsum(np.array([1, 2, 3]))
    array([1, 3, 6])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.cumsum(arr)


__all__ = ["array_cumsum"]
