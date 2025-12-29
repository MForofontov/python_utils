"""
Compute eigenvalues and eigenvectors with validation and sorting.

Uses numpy.linalg.eig, adds validation, sorting options,
and comprehensive output formatting.
"""

from typing import Literal

import numpy as np


def compute_eigenvalues(
    matrix: list[list[float]] | np.ndarray,
    sort: Literal["ascending", "descending", "magnitude", None] = None,
    return_eigenvectors: bool = True,
) -> dict[str, np.ndarray]:
    """
    Compute eigenvalues and eigenvectors with validation and sorting.

    Uses numpy.linalg.eig, adds validation, sorting options,
    and comprehensive output formatting.

    Parameters
    ----------
    matrix : list[list[float]] | np.ndarray
        Square matrix (n x n).
    sort : {'ascending', 'descending', 'magnitude', None}, optional
        Sort order for eigenvalues (by default None).
    return_eigenvectors : bool, optional
        Whether to return eigenvectors (by default True).

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary containing:
        - eigenvalues: Array of eigenvalues
        - eigenvectors: Matrix of eigenvectors (if requested)

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If matrix is not square or contains invalid values.

    Examples
    --------
    >>> matrix = [[1, 2], [2, 1]]
    >>> result = compute_eigenvalues(matrix, sort='descending')
    >>> result['eigenvalues']
    array([3., -1.])

    Notes
    -----
    For symmetric matrices, eigenvalues are real. For non-symmetric
    matrices, eigenvalues may be complex.

    Complexity
    ----------
    Time: O(n³), Space: O(n²)
    """
    # Input validation
    if not isinstance(matrix, (list, np.ndarray)):
        raise TypeError(
            f"matrix must be a list or numpy array, got {type(matrix).__name__}"
        )
    if sort is not None and not isinstance(sort, str):
        raise TypeError(f"sort must be a string or None, got {type(sort).__name__}")
    if sort is not None and sort not in ("ascending", "descending", "magnitude"):
        raise ValueError(
            f"sort must be 'ascending', 'descending', 'magnitude', or None, got '{sort}'"
        )
    if not isinstance(return_eigenvectors, bool):
        raise TypeError(
            f"return_eigenvectors must be a boolean, got {type(return_eigenvectors).__name__}"
        )

    # Convert to numpy array
    try:
        mat = np.asarray(matrix, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"matrix contains non-numeric values: {e}") from e

    # Validate dimensions
    if mat.ndim != 2:
        raise ValueError(f"matrix must be 2-dimensional, got {mat.ndim} dimensions")
    if mat.shape[0] != mat.shape[1]:
        raise ValueError(f"matrix must be square, got shape {mat.shape}")

    # Check for NaN or Inf
    if np.any(~np.isfinite(mat)):
        raise ValueError("matrix contains NaN or Inf values")

    # Compute eigenvalues and eigenvectors
    try:
        if return_eigenvectors:
            eigenvalues, eigenvectors = np.linalg.eig(mat)
        else:
            eigenvalues = np.linalg.eigvals(mat)
            eigenvectors = None
    except np.linalg.LinAlgError as e:
        raise ValueError(f"failed to compute eigenvalues: {e}") from e

    # Sort if requested
    if sort is not None:
        if sort == "ascending":
            idx = np.argsort(eigenvalues.real)
        elif sort == "descending":
            idx = np.argsort(eigenvalues.real)[::-1]
        elif sort == "magnitude":
            idx = np.argsort(np.abs(eigenvalues))[::-1]
        else:
            raise ValueError(f"Unknown sort option: {sort}")

        eigenvalues = eigenvalues[idx]
        if eigenvectors is not None:
            eigenvectors = eigenvectors[:, idx]

    result = {"eigenvalues": eigenvalues}
    if eigenvectors is not None:
        result["eigenvectors"] = eigenvectors

    return result


__all__ = ["compute_eigenvalues"]
