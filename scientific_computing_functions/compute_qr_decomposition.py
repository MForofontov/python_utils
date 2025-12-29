"""
Perform QR decomposition with validation and applications.

Uses numpy.linalg.qr, adds validation and convenient access
to Q and R matrices with orthogonality verification.
"""

from typing import Literal

import numpy as np


def compute_qr_decomposition(
    matrix: list[list[float]] | np.ndarray,
    mode: Literal["reduced", "complete"] = "reduced",
    verify_orthogonal: bool = True,
) -> dict[str, np.ndarray | bool]:
    """
    Perform QR decomposition with validation and verification.

    Uses numpy.linalg.qr, adds validation and orthogonality verification.

    Parameters
    ----------
    matrix : list[list[float]] | np.ndarray
        Matrix to decompose (m x n).
    mode : {'reduced', 'complete'}, optional
        QR decomposition mode (by default 'reduced').
    verify_orthogonal : bool, optional
        Whether to verify Q is orthogonal (by default True).

    Returns
    -------
    dict[str, np.ndarray | bool]
        Dictionary containing:
        - Q: Orthogonal matrix
        - R: Upper triangular matrix
        - is_orthogonal: Whether Q is orthogonal (if verified)

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If matrix contains invalid values.

    Examples
    --------
    >>> matrix = [[1, 2], [3, 4], [5, 6]]
    >>> result = compute_qr_decomposition(matrix)
    >>> result['Q'].shape
    (3, 2)
    >>> result['R'].shape
    (2, 2)

    Notes
    -----
    QR decomposition is useful for solving least squares problems,
    computing eigenvalues, and orthogonalization.

    Complexity
    ----------
    Time: O(mn²), Space: O(mn)
    """
    # Input validation
    if not isinstance(matrix, (list, np.ndarray)):
        raise TypeError(
            f"matrix must be a list or numpy array, got {type(matrix).__name__}"
        )
    if not isinstance(mode, str):
        raise TypeError(f"mode must be a string, got {type(mode).__name__}")
    if mode not in ("reduced", "complete"):
        raise ValueError(f"mode must be 'reduced' or 'complete', got '{mode}'")
    if not isinstance(verify_orthogonal, bool):
        raise TypeError(
            f"verify_orthogonal must be a boolean, got {type(verify_orthogonal).__name__}"
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

    # Compute QR decomposition
    try:
        Q, R = np.linalg.qr(mat, mode=mode)
    except np.linalg.LinAlgError as e:
        raise ValueError(f"failed to compute QR decomposition: {e}") from e

    result = {
        "Q": Q,
        "R": R,
    }

    # Verify orthogonality of Q
    if verify_orthogonal:
        # Q should satisfy Q^T Q = I
        QtQ = Q.T @ Q
        identity = np.eye(QtQ.shape[0])
        is_orthogonal = np.allclose(QtQ, identity, atol=1e-10)
        result["is_orthogonal"] = is_orthogonal

    return result


__all__ = ["compute_qr_decomposition"]
