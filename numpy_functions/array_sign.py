import numpy as np


def array_sign(arr: np.ndarray) -> np.ndarray:
    """
    Compute the sign of each element in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Array containing the sign of each element in ``arr`` (-1, 0, or 1).

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.

    Examples
    --------
    >>> array_sign(np.array([-2.5, 0.0, 3.1]))
    array([-1.,  0.,  1.])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.sign(arr)


__all__ = ["array_sign"]
