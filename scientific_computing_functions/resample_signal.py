"""
Resample signal to different sampling rate with validation.

Uses scipy.signal.resample, adds validation, anti-aliasing,
and comprehensive resampling workflow.
"""

import numpy as np
from scipy import signal


def resample_signal(
    data: list[float] | np.ndarray,
    original_rate: float,
    target_rate: float,
    method: str = "fourier",
) -> dict[str, np.ndarray | float]:
    """
    Resample signal to different sampling rate with validation.

    Uses scipy.signal.resample, adds validation and comprehensive output.

    Parameters
    ----------
    data : list[float] | np.ndarray
        Input signal to resample.
    original_rate : float
        Original sampling rate in Hz.
    target_rate : float
        Target sampling rate in Hz.
    method : str, optional
        Resampling method: 'fourier' or 'polyphase' (by default 'fourier').

    Returns
    -------
    dict[str, np.ndarray | float]
        Dictionary containing:
        - resampled_signal: Resampled output signal
        - original_length: Original signal length
        - resampled_length: Resampled signal length
        - resampling_ratio: Ratio of target to original rate

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or sampling rates are invalid.

    Examples
    --------
    >>> data = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> result = resample_signal(data, original_rate=8, target_rate=4)
    >>> len(result['resampled_signal'])
    4

    Notes
    -----
    Fourier method uses FFT for resampling.
    For downsampling, anti-aliasing filter is applied.

    Complexity
    ----------
    Time: O(n log n), Space: O(n)
    """
    # Input validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(
            f"data must be a list or numpy array, got {type(data).__name__}"
        )
    if not isinstance(original_rate, (int, float)):
        raise TypeError(
            f"original_rate must be a number, got {type(original_rate).__name__}"
        )
    if not isinstance(target_rate, (int, float)):
        raise TypeError(
            f"target_rate must be a number, got {type(target_rate).__name__}"
        )
    if not isinstance(method, str):
        raise TypeError(f"method must be a string, got {type(method).__name__}")
    if method not in ("fourier", "polyphase"):
        raise ValueError(f"method must be 'fourier' or 'polyphase', got '{method}'")
    if original_rate <= 0:
        raise ValueError(f"original_rate must be positive, got {original_rate}")
    if target_rate <= 0:
        raise ValueError(f"target_rate must be positive, got {target_rate}")

    # Convert to numpy array
    try:
        arr = np.asarray(data, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"data contains non-numeric values: {e}") from e

    if arr.ndim != 1:
        raise ValueError(f"data must be 1-dimensional, got {arr.ndim} dimensions")
    if arr.size == 0:
        raise ValueError("data cannot be empty")

    # Remove NaN values
    arr = arr[~np.isnan(arr)]
    if arr.size == 0:
        raise ValueError("data contains only NaN values")

    # Calculate new number of samples
    original_length = arr.size
    resampling_ratio = target_rate / original_rate
    target_length = int(np.round(original_length * resampling_ratio))

    if target_length < 1:
        raise ValueError(
            f"resampling results in < 1 sample (target_length={target_length})"
        )

    # Resample signal
    try:
        if method == "fourier":
            resampled = signal.resample(arr, target_length)
        elif method == "polyphase":
            resampled = signal.resample_poly(arr, target_rate, original_rate)
            target_length = resampled.size
        else:
            raise ValueError(f"Unknown method: {method}")
    except Exception as e:
        raise ValueError(f"failed to resample signal: {e}") from e

    return {
        "resampled_signal": resampled,
        "original_length": int(original_length),
        "resampled_length": int(target_length),
        "resampling_ratio": float(resampling_ratio),
        "original_rate": float(original_rate),
        "target_rate": float(target_rate),
    }


__all__ = ["resample_signal"]
