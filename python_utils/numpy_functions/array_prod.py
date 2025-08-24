import numpy as np


def array_prod(arr: np.ndarray) -> float:
    """
    Compute the product of all elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    float
        The product of all elements in the array.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.

    Examples
    --------
    >>> array_prod(np.array([1, 2, 3]))
    6.0
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return float(np.prod(arr))


__all__ = ["array_prod"]
