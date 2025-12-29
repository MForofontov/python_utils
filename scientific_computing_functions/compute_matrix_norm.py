"""
Compute matrix norm with validation and multiple norm types.

Uses numpy.linalg.norm, adds validation and convenient access
to different norm types.
"""

from typing import Literal

import numpy as np


def compute_matrix_norm(
    matrix: list[list[float]] | np.ndarray,
    norm_type: Literal["fro", "nuc", "1", "2", "inf"] = "fro",
) -> float:
    """
    Compute matrix norm with validation and multiple norm types.

    Uses numpy.linalg.norm, adds validation and convenient access
    to different norm types.

    Parameters
    ----------
    matrix : list[list[float]] | np.ndarray
        Matrix to compute norm for.
    norm_type : {'fro', 'nuc', '1', '2', 'inf'}, optional
        Type of matrix norm (by default 'fro').
        - 'fro': Frobenius norm
        - 'nuc': Nuclear norm (sum of singular values)
        - '1': 1-norm (max column sum)
        - '2': 2-norm (largest singular value)
        - 'inf': Infinity norm (max row sum)

    Returns
    -------
    float
        Matrix norm value.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If matrix contains invalid values.

    Examples
    --------
    >>> matrix = [[1, 2], [3, 4]]
    >>> compute_matrix_norm(matrix, norm_type='fro')
    5.477225575051661

    Notes
    -----
    Different norms are useful for different applications:
    - Frobenius: Most commonly used, easy to compute
    - Nuclear: Useful for low-rank matrix approximation
    - 2-norm: Measures maximum stretching

    Complexity
    ----------
    Time: O(mn) for most norms, O(min(m²n, mn²)) for nuclear norm
    Space: O(1)
    """
    # Input validation
    if not isinstance(matrix, (list, np.ndarray)):
        raise TypeError(
            f"matrix must be a list or numpy array, got {type(matrix).__name__}"
        )
    if not isinstance(norm_type, str):
        raise TypeError(f"norm_type must be a string, got {type(norm_type).__name__}")
    if norm_type not in ("fro", "nuc", "1", "2", "inf"):
        raise ValueError(
            f"norm_type must be 'fro', 'nuc', '1', '2', or 'inf', got '{norm_type}'"
        )

    # Convert to numpy array
    try:
        mat = np.asarray(matrix, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"matrix contains non-numeric values: {e}") from e

    # Validate dimensions
    if mat.ndim != 2:
        raise ValueError(f"matrix must be 2-dimensional, got {mat.ndim} dimensions")

    # Check for NaN or Inf
    if np.any(~np.isfinite(mat)):
        raise ValueError("matrix contains NaN or Inf values")

    # Compute norm
    try:
        if norm_type == "1":
            norm_value = np.linalg.norm(mat, ord=1)
        elif norm_type == "2":
            norm_value = np.linalg.norm(mat, ord=2)
        elif norm_type == "inf":
            norm_value = np.linalg.norm(mat, ord=np.inf)
        else:
            norm_value = np.linalg.norm(mat, ord=norm_type)
    except (np.linalg.LinAlgError, ValueError) as e:
        raise ValueError(f"failed to compute norm: {e}") from e

    return float(norm_value)


__all__ = ["compute_matrix_norm"]
