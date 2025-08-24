import numpy as np


def array_argmin(arr: np.ndarray) -> int:
    """
    Compute the index of the minimum value in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    int
        Index of the minimum value in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_argmin(np.array([1, -2, 3]))
    1
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return int(np.argmin(arr))


__all__ = ["array_argmin"]
