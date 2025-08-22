import numpy as np


def array_max(arr: np.ndarray) -> float:
    """
    Compute the maximum value in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    float
        The maximum value in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_max(np.array([1, 2, 3]))
    3.0
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return float(np.max(arr))


__all__ = ["array_max"]
