import numpy as np


def array_argmax(arr: np.ndarray) -> int:
    """
    Compute the index of the maximum value in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    int
        Index of the maximum value in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_argmax(np.array([1, 3, 2]))
    1
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return int(np.argmax(arr))


__all__ = ["array_argmax"]
