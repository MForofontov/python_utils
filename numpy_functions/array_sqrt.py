import numpy as np


def array_sqrt(arr: np.ndarray) -> np.ndarray:
    """
    Compute the element-wise square root of a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing non-negative numbers.

    Returns
    -------
    np.ndarray
        Array containing the square roots of the elements in ``arr``.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.
    ValueError
        If ``arr`` contains negative values.

    Examples
    --------
    >>> array_sqrt(np.array([0, 1, 4]))
    array([0., 1., 2.])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    if np.any(arr < 0):
        raise ValueError("arr must not contain negative values.")
    return np.sqrt(arr)


__all__ = ["array_sqrt"]

