import numpy as np


def array_clip(arr: np.ndarray, a_min: float, a_max: float) -> np.ndarray:
    """
    Clip the values in a NumPy array to a specified range.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values to be clipped.
    a_min : float
        Minimum allowed value.
    a_max : float
        Maximum allowed value.

    Returns
    -------
    np.ndarray
        Array with values clipped between ``a_min`` and ``a_max``.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.
    ValueError
        If ``a_min`` is greater than ``a_max``.

    Examples
    --------
    >>> array_clip(np.array([-1, 0, 5]), 0, 4)
    array([0, 0, 4])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    if a_min > a_max:
        raise ValueError("a_min must be less than or equal to a_max.")
    return np.clip(arr, a_min, a_max)


__all__ = ["array_clip"]

