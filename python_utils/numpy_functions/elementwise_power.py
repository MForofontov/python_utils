import numpy as np


def elementwise_power(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """
    Raise elements of one array to the powers of the corresponding elements of another array.

    Parameters
    ----------
    arr1 : np.ndarray
        The base array.
    arr2 : np.ndarray
        The exponent array.

    Returns
    -------
    np.ndarray
        Array where each element is ``arr1`` raised to the power of the corresponding element in ``arr2``.

    Raises
    ------
    TypeError
        If either input is not a NumPy ndarray.
    ValueError
        If the arrays do not have the same shape.

    Examples
    --------
    >>> elementwise_power(np.array([2, 3]), np.array([3, 2]))
    array([8, 9])
    """
    if not isinstance(arr1, np.ndarray) or not isinstance(arr2, np.ndarray):
        raise TypeError("Both inputs must be numpy.ndarray.")
    if arr1.shape != arr2.shape:
        raise ValueError("Arrays must have the same shape.")
    return np.power(arr1, arr2)


__all__ = ["elementwise_power"]
