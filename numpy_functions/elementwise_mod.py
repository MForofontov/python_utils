import numpy as np


def elementwise_mod(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """
    Compute the element-wise modulus of two NumPy arrays.

    Parameters
    ----------
    arr1 : np.ndarray
        The dividend array.
    arr2 : np.ndarray
        The divisor array.

    Returns
    -------
    np.ndarray
        Array containing the element-wise modulus of ``arr1`` and ``arr2``.

    Raises
    ------
    TypeError
        If either input is not a NumPy ndarray.
    ValueError
        If the arrays do not have the same shape.

    Examples
    --------
    >>> elementwise_mod(np.array([5, 7]), np.array([2, 3]))
    array([1, 1])
    """
    if not isinstance(arr1, np.ndarray) or not isinstance(arr2, np.ndarray):
        raise TypeError("Both inputs must be numpy.ndarray.")
    if arr1.shape != arr2.shape:
        raise ValueError("Arrays must have the same shape.")
    return np.mod(arr1, arr2)


__all__ = ["elementwise_mod"]
