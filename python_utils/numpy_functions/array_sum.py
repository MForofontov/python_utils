import numpy as np


def array_sum(arr: np.ndarray) -> float:
    """
    Compute the sum of all elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    float
        The sum of all elements in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_sum(np.array([1, 2, 3]))
    6.0
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return float(np.sum(arr))


__all__ = ["array_sum"]
