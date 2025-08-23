import numpy as np


def elementwise_greater(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """
    Compare two NumPy arrays element-wise to check if elements of ``arr1`` are greater than those of ``arr2``.

    Parameters
    ----------
    arr1 : np.ndarray
        The first input array.
    arr2 : np.ndarray
        The second input array.

    Returns
    -------
    np.ndarray
        Boolean array where each element indicates whether the corresponding
        element of ``arr1`` is greater than that of ``arr2``.

    Raises
    ------
    TypeError
        If either input is not a NumPy ndarray.
    ValueError
        If the arrays do not have the same shape.

    Examples
    --------
    >>> elementwise_greater(np.array([2, 3]), np.array([1, 4]))
    array([ True, False])
    """
    if not isinstance(arr1, np.ndarray) or not isinstance(arr2, np.ndarray):
        raise TypeError("Both inputs must be numpy.ndarray.")
    if arr1.shape != arr2.shape:
        raise ValueError("Arrays must have the same shape.")
    return np.greater(arr1, arr2)


__all__ = ["elementwise_greater"]
