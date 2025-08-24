import numpy as np


def matrix_multiply(mat1: np.ndarray, mat2: np.ndarray) -> np.ndarray:
    """
    Multiply two 2-D NumPy arrays using matrix multiplication.

    Parameters
    ----------
    mat1 : np.ndarray
        First matrix with shape (m, n).
    mat2 : np.ndarray
        Second matrix with shape (n, p).

    Returns
    -------
    np.ndarray
        The matrix product of ``mat1`` and ``mat2``.

    Raises
    ------
    TypeError
        If either input is not a NumPy ndarray.
    ValueError
        If inputs are not two-dimensional or shapes are incompatible.

    Examples
    --------
    >>> matrix_multiply(np.array([[1, 2], [3, 4]]), np.array([[5], [6]]))
    array([[17],
           [39]])
    """
    if not isinstance(mat1, np.ndarray) or not isinstance(mat2, np.ndarray):
        raise TypeError("Both inputs must be numpy.ndarray.")
    if mat1.ndim != 2 or mat2.ndim != 2:
        raise ValueError("Both arrays must be two-dimensional.")
    if mat1.shape[1] != mat2.shape[0]:
        raise ValueError("Shapes are not aligned for matrix multiplication.")
    return np.matmul(mat1, mat2)


__all__ = ["matrix_multiply"]
