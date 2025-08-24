import numpy as np


def array_mean(arr: np.ndarray) -> float:
    """
    Compute the arithmetic mean of all elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    float
        The mean of all elements in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_mean(np.array([1, 2, 3, 4]))
    2.5
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return float(np.mean(arr))


__all__ = ["array_mean"]
