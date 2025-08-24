import numpy as np


def array_diff(arr: np.ndarray) -> np.ndarray:
    """
    Compute the discrete difference between consecutive elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Array of the differences between consecutive elements.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_diff(np.array([1, 4, 9]))
    array([3, 5])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.diff(arr)


__all__ = ["array_diff"]
