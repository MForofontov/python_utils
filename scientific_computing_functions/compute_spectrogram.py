"""
Compute spectrogram for time-frequency analysis.

Uses scipy.signal.spectrogram, adds validation and convenient
parameter handling for time-frequency visualization.
"""

from typing import Literal

import numpy as np
from scipy import signal


def compute_spectrogram(
    data: list[float] | np.ndarray,
    sampling_rate: float = 1.0,
    window: Literal["hann", "hamming", "blackman", "boxcar"] = "hann",
    nperseg: int | None = None,
    noverlap: int | None = None,
    return_db: bool = True,
) -> dict[str, np.ndarray]:
    """
    Compute spectrogram for time-frequency analysis.

    Uses scipy.signal.spectrogram, adds validation and convenient
    parameter handling for time-frequency visualization.

    Parameters
    ----------
    data : list[float] | np.ndarray
        Input signal for spectrogram computation.
    sampling_rate : float, optional
        Sampling rate in Hz (by default 1.0).
    window : {'hann', 'hamming', 'blackman', 'boxcar'}, optional
        Window function type (by default 'hann').
    nperseg : int | None, optional
        Length of each segment (by default None, uses 256).
    noverlap : int | None, optional
        Number of overlapping points (by default None, uses nperseg // 2).
    return_db : bool, optional
        Whether to return power in dB scale (by default True).

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary containing:
        - time: Time bins
        - frequencies: Frequency bins
        - spectrogram: 2D time-frequency representation
        - peak_frequency: Frequency with maximum power at each time

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or parameters are invalid.

    Examples
    --------
    >>> t = np.linspace(0, 1, 1000)
    >>> signal = np.sin(2 * np.pi * 5 * t)
    >>> result = compute_spectrogram(signal, sampling_rate=1000)
    >>> result['spectrogram'].shape[0]  # frequency bins
    129

    Notes
    -----
    Spectrogram shows how frequency content changes over time.
    Useful for analyzing non-stationary signals.

    Complexity
    ----------
    Time: O(n log m) where m is segment length, Space: O(n)
    """
    # Input validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(
            f"data must be a list or numpy array, got {type(data).__name__}"
        )
    if not isinstance(sampling_rate, (int, float)):
        raise TypeError(
            f"sampling_rate must be a number, got {type(sampling_rate).__name__}"
        )
    if sampling_rate <= 0:
        raise ValueError(f"sampling_rate must be positive, got {sampling_rate}")
    if not isinstance(window, str):
        raise TypeError(f"window must be a string, got {type(window).__name__}")
    if window not in ("hann", "hamming", "blackman", "boxcar"):
        raise ValueError(
            f"window must be 'hann', 'hamming', 'blackman', or 'boxcar', got '{window}'"
        )
    if nperseg is not None and not isinstance(nperseg, int):
        raise TypeError(
            f"nperseg must be an integer or None, got {type(nperseg).__name__}"
        )
    if noverlap is not None and not isinstance(noverlap, int):
        raise TypeError(
            f"noverlap must be an integer or None, got {type(noverlap).__name__}"
        )
    if not isinstance(return_db, bool):
        raise TypeError(
            f"return_db must be a boolean, got {type(return_db).__name__}"
        )

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

    # Set default parameters
    if nperseg is None:
        nperseg = min(256, arr.size)
    if noverlap is None:
        noverlap = nperseg // 2

    # Validate parameters
    if nperseg > arr.size:
        raise ValueError(
            f"nperseg ({nperseg}) cannot be larger than data length ({arr.size})"
        )
    if noverlap >= nperseg:
        raise ValueError(f"noverlap ({noverlap}) must be < nperseg ({nperseg})")

    # Compute spectrogram
    try:
        frequencies, time, Sxx = signal.spectrogram(
            arr,
            fs=sampling_rate,
            window=window,
            nperseg=nperseg,
            noverlap=noverlap,
        )
    except Exception as e:
        raise ValueError(f"failed to compute spectrogram: {e}") from e

    # Convert to dB scale if requested
    if return_db:
        # Avoid log(0) by adding small epsilon
        Sxx = 10 * np.log10(Sxx + 1e-10)

    # Find peak frequency at each time point
    peak_freq_idx = np.argmax(Sxx, axis=0)
    peak_frequency = frequencies[peak_freq_idx]

    return {
        "time": time,
        "frequencies": frequencies,
        "spectrogram": Sxx,
        "peak_frequency": peak_frequency,
    }


__all__ = ["compute_spectrogram"]
