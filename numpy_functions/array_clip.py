import numpy as np


def array_clip(arr: np.ndarray, min_value: float, max_value: float) -> np.ndarray:
    """
    Clip the values in a NumPy array within the specified interval.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.
    min_value : float
        Minimum allowable value.
    max_value : float
        Maximum allowable value.

    Returns
    -------
    np.ndarray
        Array with values clipped between ``min_value`` and ``max_value``.

    Raises
    ------
    TypeError
        If `arr` is not a NumPy ndarray.
    ValueError
        If ``min_value`` is greater than ``max_value``.

    Examples
    --------
    >>> array_clip(np.array([1, 2, 3, 4]), 2, 3)
    array([2, 2, 3, 3])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value.")
    return np.clip(arr, min_value, max_value)


__all__ = ["array_clip"]
