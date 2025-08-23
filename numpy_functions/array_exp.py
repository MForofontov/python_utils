import numpy as np


def array_exp(arr: np.ndarray) -> np.ndarray:
    """
    Compute the element-wise exponential of a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.

    Returns
    -------
    np.ndarray
        Array containing the exponentials of the elements in ``arr``.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.

    Examples
    --------
    >>> array_exp(np.array([0, 1]))
    array([1.        , 2.71828183])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    return np.exp(arr)


__all__ = ["array_exp"]
