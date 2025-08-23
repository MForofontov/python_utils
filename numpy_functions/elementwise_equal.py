import numpy as np


def elementwise_equal(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """
    Determine element-wise equality of two NumPy arrays.

    Parameters
    ----------
    arr1 : np.ndarray
        The first input array.
    arr2 : np.ndarray
        The second input array.

    Returns
    -------
    np.ndarray
        Boolean array where each element indicates whether elements of
        ``arr1`` and ``arr2`` are equal.

    Raises
    ------
    TypeError
        If either input is not a NumPy ndarray.
    ValueError
        If the arrays do not have the same shape.

    Examples
    --------
    >>> elementwise_equal(np.array([1, 2]), np.array([1, 3]))
    array([ True, False])
    """
    if not isinstance(arr1, np.ndarray) or not isinstance(arr2, np.ndarray):
        raise TypeError("Both inputs must be numpy.ndarray.")
    if arr1.shape != arr2.shape:
        raise ValueError("Arrays must have the same shape.")
    return np.equal(arr1, arr2)


__all__ = ["elementwise_equal"]
