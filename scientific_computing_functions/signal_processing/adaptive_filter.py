"""Design and apply adaptive filters with online learning."""

from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray


def adaptive_filter(
    signal: list[float] | NDArray[Any],
    reference: list[float] | NDArray[Any] | None = None,
    filter_length: int = 32,
    algorithm: Literal["lms", "nlms", "rls"] = "nlms",
    step_size: float = 0.01,
    forgetting_factor: float = 0.99,
) -> dict[str, Any]:
    """
    Apply adaptive filtering with online learning algorithms.

    Implements adaptive filter workflow including LMS, NLMS, and RLS algorithms
    for noise cancellation, system identification, and echo cancellation. Adds
    convergence tracking and performance metrics.

    Parameters
    ----------
    signal : list[float] | NDArray[Any]
        Input signal to filter.
    reference : list[float] | NDArray[Any] | None, optional
        Reference signal for supervised adaptation. If None, uses delayed signal (by default None).
    filter_length : int, optional
        Number of filter coefficients (by default 32).
    algorithm : Literal["lms", "nlms", "rls"], optional
        Adaptive algorithm (by default "nlms"):
        - 'lms': Least Mean Squares (simple, slow convergence)
        - 'nlms': Normalized LMS (faster, more stable)
        - 'rls': Recursive Least Squares (fast convergence, higher complexity)
    step_size : float, optional
        Step size (learning rate) for LMS/NLMS (by default 0.01).
    forgetting_factor : float, optional
        Forgetting factor for RLS (by default 0.99).

    Returns
    -------
    dict[str, Any]
        Dictionary containing:
        - filtered_signal: Output filtered signal
        - error_signal: Error between desired and filtered signal
        - filter_weights: Final filter coefficients
        - mse_history: Mean squared error over time
        - convergence_iteration: Iteration where filter converged

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values or dimensions incompatible.

    Examples
    --------
    >>> signal = [0.5, 0.3, 0.8, 0.2] * 25  # 100 samples
    >>> result = adaptive_filter(signal, filter_length=8, algorithm='nlms')
    >>> len(result['filtered_signal']) == 100
    True

    >>> result = adaptive_filter(signal, algorithm='rls')
    >>> result['convergence_iteration'] is not None
    True

    Notes
    -----
    Adaptive filters learn optimal coefficients online without prior knowledge
    of signal statistics. Applications include:
    - Noise cancellation in audio/biomedical signals
    - Echo cancellation in telecommunications
    - Channel equalization
    - System identification

    LMS: Simple but sensitive to signal power
    NLMS: Normalizes by input power, more stable
    RLS: Fastest convergence but O(N^2) complexity

    Complexity
    ----------
    Time: O(N*L) for LMS/NLMS, O(N*L^2) for RLS. Space: O(L)
    where N is signal length, L is filter length.
    """
    # Input validation
    if not isinstance(signal, (list, np.ndarray)):
        raise TypeError(
            f"signal must be a list or numpy array, got {type(signal).__name__}"
        )
    if reference is not None and not isinstance(reference, (list, np.ndarray)):
        raise TypeError(
            f"reference must be a list, numpy array, or None, got {type(reference).__name__}"
        )
    if not isinstance(filter_length, int):
        raise TypeError(
            f"filter_length must be an integer, got {type(filter_length).__name__}"
        )
    if not isinstance(algorithm, str):
        raise TypeError(f"algorithm must be a string, got {type(algorithm).__name__}")
    if not isinstance(step_size, (int, float)):
        raise TypeError(f"step_size must be a number, got {type(step_size).__name__}")
    if not isinstance(forgetting_factor, (int, float)):
        raise TypeError(
            f"forgetting_factor must be a number, got {type(forgetting_factor).__name__}"
        )

    signal_array = np.asarray(signal, dtype=float)

    if signal_array.ndim != 1:
        raise ValueError(f"signal must be 1D, got shape {signal_array.shape}")
    if signal_array.size == 0:
        raise ValueError("signal cannot be empty")
    if filter_length <= 0:
        raise ValueError(f"filter_length must be positive, got {filter_length}")
    if filter_length > len(signal_array):
        raise ValueError(
            f"filter_length ({filter_length}) cannot exceed signal length ({len(signal_array)})"
        )
    if algorithm not in ["lms", "nlms", "rls"]:
        raise ValueError(
            f"Invalid algorithm: {algorithm}. Must be 'lms', 'nlms', or 'rls'"
        )
    if step_size <= 0:
        raise ValueError(f"step_size must be positive, got {step_size}")
    if not 0 < forgetting_factor <= 1:
        raise ValueError(
            f"forgetting_factor must be in (0, 1], got {forgetting_factor}"
        )

    # Create reference signal if not provided (use delayed signal)
    if reference is None:
        reference_array = np.roll(signal_array, filter_length // 2)
    else:
        reference_array = np.asarray(reference, dtype=float)
        if reference_array.shape != signal_array.shape:
            raise ValueError("reference must have same length as signal")

    n_samples = len(signal_array)
    weights = np.zeros(filter_length)
    filtered_signal = np.zeros(n_samples)
    error_signal = np.zeros(n_samples)
    mse_history = []

    # RLS-specific initialization
    if algorithm == "rls":
        P = np.eye(filter_length) / 0.01  # Inverse correlation matrix

    convergence_iteration = None
    convergence_threshold = 0.01
    window_size = min(50, n_samples // 10)

    for n in range(filter_length, n_samples):
        # Extract input vector
        x = signal_array[n - filter_length : n][::-1]

        # Filter output
        y = np.dot(weights, x)
        filtered_signal[n] = y

        # Error calculation
        d = reference_array[n]  # Desired signal
        e = d - y
        error_signal[n] = e

        # Update filter weights based on algorithm
        if algorithm == "lms":
            weights += step_size * e * x

        elif algorithm == "nlms":
            # Normalized LMS
            norm_factor = np.dot(x, x) + 1e-10  # Avoid division by zero
            weights += (step_size / norm_factor) * e * x

        elif algorithm == "rls":
            # Recursive Least Squares
            pi = np.dot(P, x)
            k = pi / (forgetting_factor + np.dot(x, pi))
            weights += k * e
            P = (P - np.outer(k, pi)) / forgetting_factor

        # Track MSE
        mse = e**2
        mse_history.append(mse)

        # Check convergence (MSE stabilizes)
        if convergence_iteration is None and n > filter_length + window_size:
            recent_mse = mse_history[-window_size:]
            mse_variance = np.var(recent_mse)
            if mse_variance < convergence_threshold:
                convergence_iteration = n

    return {
        "filtered_signal": filtered_signal,
        "error_signal": error_signal,
        "filter_weights": weights,
        "mse_history": np.array(mse_history),
        "convergence_iteration": convergence_iteration,
    }


__all__ = ["adaptive_filter"]
