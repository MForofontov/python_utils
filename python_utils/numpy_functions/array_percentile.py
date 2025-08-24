import numpy as np


def array_percentile(arr: np.ndarray, q: float) -> float:
    """
    Compute the ``q``th percentile of elements in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        Array containing numerical values.
    q : float
        Percentile to compute, between 0 and 100 inclusive.

    Returns
    -------
    float
        The ``q``th percentile of the array.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray or ``q`` is not a numeric type.
    ValueError
        If ``q`` is outside the range [0, 100].

    Examples
    --------
    >>> array_percentile(np.array([1, 2, 3, 4]), 50)
    2.5
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    if not isinstance(q, (int, float)):
        raise TypeError("q must be a float or int.")
    if q < 0 or q > 100:
        raise ValueError("q must be between 0 and 100.")
    return float(np.percentile(arr, q))


__all__ = ["array_percentile"]
