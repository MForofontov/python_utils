import numpy as np


def array_min(arr: np.ndarray) -> float:
    """
    Compute the minimum value in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    float
        The minimum value in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_min(np.array([1, 2, 3]))
    1.0
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return float(np.min(arr))


__all__ = ["array_min"]
