import numpy as np


def array_floor(arr: np.ndarray) -> np.ndarray:
    """
    Compute the floor of each element in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Array containing the floor of each element in ``arr``.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.

    Examples
    --------
    >>> array_floor(np.array([1.5, -2.3]))
    array([ 1., -3.])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.floor(arr)


__all__ = ["array_floor"]
