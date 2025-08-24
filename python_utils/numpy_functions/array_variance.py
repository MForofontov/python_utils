import numpy as np


def array_variance(arr: np.ndarray) -> float:
    """
    Compute the variance of all elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    float
        The variance of all elements in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_variance(np.array([1, 3]))
    1.0
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return float(np.var(arr))


__all__ = ["array_variance"]
