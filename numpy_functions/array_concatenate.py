import numpy as np
from collections.abc import Sequence


def array_concatenate(arrays: Sequence[np.ndarray], axis: int = 0) -> np.ndarray:
    """
    Concatenate a sequence of NumPy arrays along a specified axis.

    Parameters
    ----------
    arrays : Sequence[np.ndarray]
        Sequence of NumPy arrays to concatenate. Must contain at least one array.
    axis : int, optional
        Axis along which to concatenate, by default ``0``.

    Returns
    -------
    np.ndarray
        The concatenated array.

    Raises
    ------
    TypeError
        If any element in ``arrays`` is not a NumPy ndarray.
    ValueError
        If ``arrays`` is empty.

    Examples
    --------
    >>> array_concatenate([np.array([1, 2]), np.array([3, 4])])
    array([1, 2, 3, 4])
    """
    arrays_list = list(arrays)
    if not arrays_list:
        raise ValueError("arrays must contain at least one numpy.ndarray")
    if not all(isinstance(arr, np.ndarray) for arr in arrays_list):
        raise TypeError("All items in arrays must be numpy.ndarray")
    return np.concatenate(arrays_list, axis=axis)


__all__ = ["array_concatenate"]
