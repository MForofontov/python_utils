import numpy as np


def array_std(arr: np.ndarray) -> float:
    """
    Compute the standard deviation of all elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    float
        The standard deviation of all elements in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_std(np.array([1, 3]))
    1.0
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return float(np.std(arr))


__all__ = ["array_std"]
