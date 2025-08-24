import numpy as np


def array_reshape(arr: np.ndarray, new_shape: tuple[int, ...]) -> np.ndarray:
    """
    Reshape a NumPy array to a specified ``new_shape``.

    Parameters
    ----------
    arr : np.ndarray
        The input array to reshape.
    new_shape : tuple[int, ...]
        The desired shape for the array.

    Returns
    -------
    np.ndarray
        A view or copy of the array with the new shape.

    Raises
    ------
    TypeError
        If ``arr`` is not a NumPy ndarray or ``new_shape`` is not a tuple of
        integers.
    ValueError
        If the total size of ``new_shape`` does not match the number of
        elements in ``arr`` or if more than one dimension is set to ``-1``.

    Examples
    --------
    >>> array_reshape(np.array([1, 2, 3, 4]), (2, 2))
    array([[1, 2],
           [3, 4]])
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("arr must be a numpy.ndarray.")
    if not isinstance(new_shape, tuple) or not all(isinstance(dim, int) for dim in new_shape):
        raise TypeError("new_shape must be a tuple of integers.")
    if new_shape.count(-1) > 1:
        raise ValueError("new_shape can contain at most one -1.")
    if -1 not in new_shape and np.prod(new_shape) != arr.size:
        raise ValueError(
            "The product of new_shape dimensions must equal the number of elements in arr."
        )
    return np.reshape(arr, new_shape)


__all__ = ["array_reshape"]
