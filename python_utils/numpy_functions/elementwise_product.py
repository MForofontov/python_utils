import numpy as np


def elementwise_product(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """
    Compute the element-wise product of two NumPy arrays.

    Parameters
    ----------
    arr1 : np.ndarray
        The first input array.
    arr2 : np.ndarray
        The second input array.

    Returns
    -------
    np.ndarray
        Array containing the element-wise product of ``arr1`` and ``arr2``.

    Raises
    ------
    TypeError
        If either input is not a NumPy ndarray.
    ValueError
        If the arrays do not have the same shape.

    Examples
    --------
    >>> elementwise_product(np.array([1, 2]), np.array([3, 4]))
    array([3, 8])
    """
    if not isinstance(arr1, np.ndarray) or not isinstance(arr2, np.ndarray):
        raise TypeError("Both inputs must be numpy.ndarray.")
    if arr1.shape != arr2.shape:
        raise ValueError("Arrays must have the same shape.")
    return np.multiply(arr1, arr2)


__all__ = ["elementwise_product"]
