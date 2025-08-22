import numpy as np


def array_median(arr: np.ndarray) -> float:
    """
    Compute the median of all elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    float
        The median of all elements in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_median(np.array([1, 3, 5]))
    3.0
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return float(np.median(arr))


__all__ = ["array_median"]
