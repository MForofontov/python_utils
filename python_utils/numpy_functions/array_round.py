import numpy as np


def array_round(arr: np.ndarray, decimals: int = 0) -> np.ndarray:
    """
    Round each element in a NumPy array to the specified number of decimals.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.
    decimals : int, optional
        Number of decimal places to round to, by default 0.

    Returns
    -------
    np.ndarray
        Array with elements rounded to ``decimals`` places.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray or ``decimals`` is not an integer.

    Examples
    --------
    >>> array_round(np.array([1.234, 5.678]), 2)
    array([1.23, 5.68])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    if not isinstance(decimals, int):
        raise TypeError("decimals must be an integer.")
    return np.round(arr, decimals)


__all__ = ["array_round"]
