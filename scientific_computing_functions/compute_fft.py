"""
Compute Fast Fourier Transform with validation and frequency analysis.

Uses numpy.fft, adds validation, frequency calculation,
and comprehensive spectral analysis output.
"""

import numpy as np


def compute_fft(
    signal: list[float] | np.ndarray,
    sampling_rate: float = 1.0,
    return_magnitude: bool = True,
    return_phase: bool = False,
    normalize: bool = False,
) -> dict[str, np.ndarray]:
    """
    Compute Fast Fourier Transform with validation and frequency analysis.

    Uses numpy.fft, adds validation, frequency calculation,
    and comprehensive spectral analysis output.

    Parameters
    ----------
    signal : list[float] | np.ndarray
        Input time-domain signal.
    sampling_rate : float, optional
        Sampling rate in Hz (by default 1.0).
    return_magnitude : bool, optional
        Whether to return magnitude spectrum (by default True).
    return_phase : bool, optional
        Whether to return phase spectrum (by default False).
    normalize : bool, optional
        Whether to normalize FFT by signal length (by default False).

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary containing:
        - frequencies: Frequency bins
        - fft_complex: Complex FFT coefficients
        - magnitude: Magnitude spectrum (if requested)
        - phase: Phase spectrum (if requested)
        - power: Power spectral density (if magnitude returned)

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If signal is empty or sampling_rate is invalid.

    Examples
    --------
    >>> t = np.linspace(0, 1, 100)
    >>> signal = np.sin(2 * np.pi * 5 * t)  # 5 Hz sine wave
    >>> result = compute_fft(signal, sampling_rate=100)
    >>> peak_freq_idx = np.argmax(result['magnitude'][1:]) + 1
    >>> result['frequencies'][peak_freq_idx]
    5.0

    Notes
    -----
    FFT converts time-domain signal to frequency domain.
    Returns only positive frequencies (one-sided spectrum).

    Complexity
    ----------
    Time: O(n log n), Space: O(n)
    """
    # Input validation
    if not isinstance(signal, (list, np.ndarray)):
        raise TypeError(
            f"signal must be a list or numpy array, got {type(signal).__name__}"
        )
    if not isinstance(sampling_rate, (int, float)):
        raise TypeError(
            f"sampling_rate must be a number, got {type(sampling_rate).__name__}"
        )
    if sampling_rate <= 0:
        raise ValueError(f"sampling_rate must be positive, got {sampling_rate}")
    if not isinstance(return_magnitude, bool):
        raise TypeError(
            f"return_magnitude must be a boolean, got {type(return_magnitude).__name__}"
        )
    if not isinstance(return_phase, bool):
        raise TypeError(
            f"return_phase must be a boolean, got {type(return_phase).__name__}"
        )
    if not isinstance(normalize, bool):
        raise TypeError(
            f"normalize must be a boolean, got {type(normalize).__name__}"
        )

    # Convert to numpy array
    try:
        arr = np.asarray(signal, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"signal contains non-numeric values: {e}") from e

    if arr.ndim != 1:
        raise ValueError(f"signal must be 1-dimensional, got {arr.ndim} dimensions")
    if arr.size == 0:
        raise ValueError("signal cannot be empty")

    # Remove NaN values
    arr = arr[~np.isnan(arr)]
    if arr.size == 0:
        raise ValueError("signal contains only NaN values")

    # Compute FFT
    fft_result = np.fft.fft(arr)

    if normalize:
        fft_result = fft_result / arr.size

    # Compute frequency bins
    n = arr.size
    frequencies = np.fft.fftfreq(n, d=1.0 / sampling_rate)

    # Get positive frequencies only (one-sided spectrum)
    positive_freq_idx = frequencies >= 0
    frequencies = frequencies[positive_freq_idx]
    fft_result = fft_result[positive_freq_idx]

    result = {
        "frequencies": frequencies,
        "fft_complex": fft_result,
    }

    # Compute magnitude spectrum
    if return_magnitude:
        magnitude = np.abs(fft_result)
        result["magnitude"] = magnitude
        # Power spectral density (magnitude squared)
        result["power"] = magnitude ** 2

    # Compute phase spectrum
    if return_phase:
        phase = np.angle(fft_result)
        result["phase"] = phase

    return result


__all__ = ["compute_fft"]
