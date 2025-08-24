import numpy as np


def elementwise_divide(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """
    Compute the element-wise division of two NumPy arrays.

    Parameters
    ----------
    arr1 : np.ndarray
        The numerator array.
    arr2 : np.ndarray
        The denominator array.

    Returns
    -------
    np.ndarray
        Array containing the element-wise division of ``arr1`` by ``arr2``.

    Raises
    ------
    TypeError
        If either input is not a NumPy ndarray.
    ValueError
        If the arrays do not have the same shape or if ``arr2`` contains zeros.

    Examples
    --------
    >>> elementwise_divide(np.array([2, 4]), np.array([1, 2]))
    array([2., 2.])
    """
    if not isinstance(arr1, np.ndarray) or not isinstance(arr2, np.ndarray):
        raise TypeError("Both inputs must be numpy.ndarray.")
    if arr1.shape != arr2.shape:
        raise ValueError("Arrays must have the same shape.")
    if np.any(arr2 == 0):
        raise ValueError("arr2 must not contain zeros.")
    return np.divide(arr1, arr2)


__all__ = ["elementwise_divide"]
