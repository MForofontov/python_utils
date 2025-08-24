import numpy as np


def array_ceil(arr: np.ndarray) -> np.ndarray:
    """
    Compute the ceiling of each element in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Array containing the ceiling of each element in ``arr``.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.

    Examples
    --------
    >>> array_ceil(np.array([1.2, -2.7, 0.0]))
    array([ 2., -2.,  0.])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.ceil(arr)


__all__ = ["array_ceil"]
