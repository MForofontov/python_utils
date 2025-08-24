import numpy as np


def normalize_array(arr: np.ndarray) -> np.ndarray:
    """
    Normalize a NumPy array so that its Euclidean norm is 1.

    Parameters
    ----------
    arr : np.ndarray
        Input array to normalize.

    Returns
    -------
    np.ndarray
        The normalized array with unit Euclidean norm.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray.
    ValueError
        If the norm of ``arr`` is zero.

    Examples
    --------
    >>> normalize_array(np.array([3, 4]))
    array([0.6, 0.8])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    norm = np.linalg.norm(arr)
    if norm == 0:
        raise ValueError("Cannot normalize an array with zero norm.")
    return arr / norm


__all__ = ["normalize_array"]
