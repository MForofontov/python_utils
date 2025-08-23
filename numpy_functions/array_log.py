import numpy as np


def array_log(arr: np.ndarray) -> np.ndarray:
    """
    Compute the element-wise natural logarithm of a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing positive numbers.

    Returns
    -------
    np.ndarray
        Array containing the natural logarithm of the elements in ``arr``.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.
    ValueError
        If ``arr`` contains non-positive values.

    Examples
    --------
    >>> array_log(np.array([1, np.e]))
    array([0., 1.])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    if np.any(arr <= 0):
        raise ValueError("arr must contain only positive values.")
    return np.log(arr)


__all__ = ["array_log"]
