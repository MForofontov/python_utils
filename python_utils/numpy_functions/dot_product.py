import numpy as np


def dot_product(arr1: np.ndarray, arr2: np.ndarray) -> float:
    """
    Compute the dot product of two one-dimensional NumPy arrays.

    Parameters
    ----------
    arr1 : np.ndarray
        The first input array.
    arr2 : np.ndarray
        The second input array.

    Returns
    -------
    float
        The dot product of the two arrays.

    Raises
    ------
    TypeError
        If either input is not a NumPy ndarray.
    ValueError
        If the arrays are not one-dimensional or have different shapes.

    Examples
    --------
    >>> dot_product(np.array([1, 2, 3]), np.array([4, 5, 6]))
    32.0
    """
    if not isinstance(arr1, np.ndarray) or not isinstance(arr2, np.ndarray):
        raise TypeError("Both inputs must be numpy.ndarray.")
    if arr1.ndim != 1 or arr2.ndim != 1 or arr1.shape != arr2.shape:
        raise ValueError("Arrays must be one-dimensional with the same shape.")
    return float(np.dot(arr1, arr2))


__all__ = ["dot_product"]
