import numpy as np


def array_abs(arr: np.ndarray) -> np.ndarray:
    """
    Compute the absolute value of each element in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Array containing the absolute values of ``arr``.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.

    Examples
    --------
    >>> array_abs(np.array([-1, 2, -3]))
    array([1, 2, 3])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.abs(arr)


__all__ = ["array_abs"]
