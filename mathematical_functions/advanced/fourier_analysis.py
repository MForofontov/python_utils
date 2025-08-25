"""
Fourier analysis and transform functions.

This module provides discrete and continuous Fourier transform implementations
and related frequency domain analysis tools.
"""

import math
import cmath
from typing import Union, List, Dict, Any, Optional, Tuple
import numpy as np


def fourier_transform(signal: Union[List[float], List[complex]],
                     method: str = 'dft',
                     inverse: bool = False,
                     sampling_rate: Optional[float] = None,
                     window: Optional[str] = None,
                     zero_padding: Optional[int] = None) -> Dict[str, Any]:
    """
    Compute Fourier transform of a signal using various methods.

    Performs discrete or fast Fourier transform on input signal with
    optional windowing and frequency analysis.

    Parameters
    ----------
    signal : list of float or complex
        Input signal samples.
    method : str, optional
        Transform method to use. Options:
        - 'dft': Discrete Fourier Transform (default)
        - 'fft': Fast Fourier Transform
        - 'dct': Discrete Cosine Transform
        - 'dst': Discrete Sine Transform
    inverse : bool, optional
        Compute inverse transform (default: False).
    sampling_rate : float, optional
        Sampling rate in Hz. If provided, frequency axis is computed.
    window : str, optional
        Windowing function to apply. Options:
        - 'hann': Hann window
        - 'hamming': Hamming window  
        - 'blackman': Blackman window
        - 'rectangular': Rectangular window (no windowing)
    zero_padding : int, optional
        Zero-pad signal to this length before transform.

    Returns
    -------
    dict
        Dictionary containing:
        - 'transform': Complex transform coefficients
        - 'magnitude': Magnitude spectrum
        - 'phase': Phase spectrum (in radians)
        - 'frequencies': Frequency axis (if sampling_rate provided)
        - 'method_used': Transform method used
        - 'n_samples': Number of samples
        - 'windowed_signal': Windowed input signal

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If parameters are invalid.

    Examples
    --------
    >>> # Analyze a simple sinusoid
    >>> import math
    >>> t = [i/100 for i in range(100)]
    >>> signal = [math.sin(2*math.pi*5*ti) for ti in t]  # 5 Hz sine wave
    >>> result = fourier_transform(signal, sampling_rate=100)
    >>> # Peak should be around 5 Hz
    >>> peak_freq_idx = result['magnitude'].index(max(result['magnitude'][1:50]))
    >>> peak_freq = result['frequencies'][peak_freq_idx]
    >>> abs(peak_freq - 5.0) < 1.0
    True

    Notes
    -----
    DFT has O(N²) complexity while FFT has O(N log N) complexity.
    Windowing reduces spectral leakage but may broaden spectral peaks.
    Zero padding increases frequency resolution but doesn't add information.
    """
    # Input validation
    if not isinstance(signal, (list, tuple)):
        raise TypeError("signal must be a list or tuple")
    if len(signal) == 0:
        raise ValueError("signal cannot be empty")
    
    # Convert to complex if needed
    signal_complex = []
    for s in signal:
        if isinstance(s, (int, float)):
            signal_complex.append(complex(s, 0))
        elif isinstance(s, complex):
            signal_complex.append(s)
        else:
            raise TypeError("signal elements must be numeric or complex")
    
    # Validate method
    valid_methods = ['dft', 'fft', 'dct', 'dst']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    method = method.lower()
    
    # Validate window
    if window is not None:
        valid_windows = ['hann', 'hamming', 'blackman', 'rectangular']
        if window.lower() not in valid_windows:
            raise ValueError(f"window must be one of {valid_windows}")
        window = window.lower()
    
    # Apply windowing
    windowed_signal = _apply_window(signal_complex, window) if window else signal_complex
    
    # Apply zero padding
    if zero_padding is not None:
        if not isinstance(zero_padding, int) or zero_padding < len(windowed_signal):
            raise ValueError("zero_padding must be integer >= signal length")
        windowed_signal.extend([0] * (zero_padding - len(windowed_signal)))
    
    N = len(windowed_signal)
    
    # Apply transform
    if method == 'dft':
        if inverse:
            transform = _inverse_dft(windowed_signal)
        else:
            transform = _dft(windowed_signal)
    elif method == 'fft':
        if inverse:
            transform = _inverse_fft(windowed_signal)
        else:
            transform = _fft(windowed_signal)
    elif method == 'dct':
        if inverse:
            transform = _inverse_dct(windowed_signal)
        else:
            transform = _dct(windowed_signal)
    elif method == 'dst':
        if inverse:
            transform = _inverse_dst(windowed_signal)
        else:
            transform = _dst(windowed_signal)
    
    # Compute magnitude and phase
    magnitude = [abs(x) for x in transform]
    phase = [cmath.phase(x) for x in transform]
    
    # Compute frequency axis
    frequencies = None
    if sampling_rate is not None:
        if not isinstance(sampling_rate, (int, float)) or sampling_rate <= 0:
            raise ValueError("sampling_rate must be positive")
        frequencies = [i * sampling_rate / N for i in range(N)]
    
    return {
        'transform': transform,
        'magnitude': magnitude,
        'phase': phase,
        'frequencies': frequencies,
        'method_used': method,
        'n_samples': N,
        'windowed_signal': windowed_signal
    }


def _apply_window(signal: List[complex], window: str) -> List[complex]:
    """Apply windowing function to signal."""
    N = len(signal)
    
    if window == 'hann':
        w = [0.5 - 0.5 * math.cos(2 * math.pi * n / (N - 1)) for n in range(N)]
    elif window == 'hamming':
        w = [0.54 - 0.46 * math.cos(2 * math.pi * n / (N - 1)) for n in range(N)]
    elif window == 'blackman':
        w = [0.42 - 0.5 * math.cos(2 * math.pi * n / (N - 1)) + 
             0.08 * math.cos(4 * math.pi * n / (N - 1)) for n in range(N)]
    else:  # rectangular
        w = [1.0] * N
    
    return [signal[i] * w[i] for i in range(N)]


def _dft(signal: List[complex]) -> List[complex]:
    """Discrete Fourier Transform implementation."""
    N = len(signal)
    X = []
    
    for k in range(N):
        sum_val = 0
        for n in range(N):
            angle = -2 * math.pi * k * n / N
            sum_val += signal[n] * cmath.exp(1j * angle)
        X.append(sum_val)
    
    return X


def _inverse_dft(X: List[complex]) -> List[complex]:
    """Inverse Discrete Fourier Transform implementation."""
    N = len(X)
    x = []
    
    for n in range(N):
        sum_val = 0
        for k in range(N):
            angle = 2 * math.pi * k * n / N
            sum_val += X[k] * cmath.exp(1j * angle)
        x.append(sum_val / N)
    
    return x


def _fft(signal: List[complex]) -> List[complex]:
    """Fast Fourier Transform using Cooley-Tukey algorithm."""
    N = len(signal)
    
    # Base case
    if N <= 1:
        return signal
    
    # Make N a power of 2 by zero-padding if necessary
    if N & (N - 1) != 0:  # Not a power of 2
        next_power = 1 << (N - 1).bit_length()
        signal = signal + [0] * (next_power - N)
        N = next_power
    
    # Divide
    even = [signal[i] for i in range(0, N, 2)]
    odd = [signal[i] for i in range(1, N, 2)]
    
    # Conquer
    y_even = _fft(even)
    y_odd = _fft(odd)
    
    # Combine
    y = [0] * N
    for k in range(N // 2):
        t = cmath.exp(-2j * math.pi * k / N) * y_odd[k]
        y[k] = y_even[k] + t
        y[k + N // 2] = y_even[k] - t
    
    return y


def _inverse_fft(X: List[complex]) -> List[complex]:
    """Inverse Fast Fourier Transform."""
    # Conjugate input
    X_conj = [x.conjugate() for x in X]
    
    # Apply FFT
    x_conj = _fft(X_conj)
    
    # Conjugate result and scale
    N = len(X)
    x = [val.conjugate() / N for val in x_conj]
    
    return x


def _dct(signal: List[complex]) -> List[complex]:
    """Discrete Cosine Transform (DCT-II) implementation."""
    N = len(signal)
    X = []
    
    for k in range(N):
        sum_val = 0
        for n in range(N):
            sum_val += signal[n].real * math.cos(math.pi * k * (2 * n + 1) / (2 * N))
        
        # Apply scaling
        if k == 0:
            sum_val *= math.sqrt(1 / N)
        else:
            sum_val *= math.sqrt(2 / N)
        
        X.append(complex(sum_val, 0))
    
    return X


def _inverse_dct(X: List[complex]) -> List[complex]:
    """Inverse Discrete Cosine Transform (DCT-III) implementation."""
    N = len(X)
    x = []
    
    for n in range(N):
        sum_val = X[0].real / math.sqrt(N)
        
        for k in range(1, N):
            sum_val += X[k].real * math.sqrt(2 / N) * math.cos(math.pi * k * (2 * n + 1) / (2 * N))
        
        x.append(complex(sum_val, 0))
    
    return x


def _dst(signal: List[complex]) -> List[complex]:
    """Discrete Sine Transform (DST-I) implementation."""
    N = len(signal)
    X = []
    
    for k in range(N):
        sum_val = 0
        for n in range(N):
            sum_val += signal[n].real * math.sin(math.pi * (k + 1) * (n + 1) / (N + 1))
        
        sum_val *= math.sqrt(2 / (N + 1))
        X.append(complex(sum_val, 0))
    
    return X


def _inverse_dst(X: List[complex]) -> List[complex]:
    """Inverse Discrete Sine Transform implementation."""
    # DST-I is its own inverse (up to scaling)
    return _dst(X)


def spectral_analysis(signal: Union[List[float], List[complex]],
                     sampling_rate: float,
                     window: str = 'hann',
                     nperseg: Optional[int] = None,
                     overlap: float = 0.5) -> Dict[str, Any]:
    """
    Perform spectral analysis using Welch's method for power spectral density.

    Computes power spectral density estimate using Welch's method with
    overlapping segments and windowing.

    Parameters
    ----------
    signal : list of float or complex
        Input signal samples.
    sampling_rate : float
        Sampling rate in Hz.
    window : str, optional
        Windowing function (default: 'hann').
    nperseg : int, optional
        Length of each segment. If None, uses len(signal)//8.
    overlap : float, optional
        Overlap fraction between segments (default: 0.5).

    Returns
    -------
    dict
        Dictionary containing:
        - 'frequencies': Frequency bins
        - 'psd': Power spectral density
        - 'peak_frequency': Dominant frequency
        - 'total_power': Total signal power
        - 'frequency_resolution': Frequency resolution

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If parameters are invalid.

    Examples
    --------
    >>> # Analyze noisy sinusoid
    >>> import math, random
    >>> signal = [math.sin(2*math.pi*10*i/100) + 0.1*random.gauss(0,1) 
    ...           for i in range(1000)]
    >>> result = spectral_analysis(signal, sampling_rate=100)
    >>> # Peak should be around 10 Hz
    >>> peak_idx = result['psd'].index(max(result['psd']))
    >>> peak_freq = result['frequencies'][peak_idx]
    >>> abs(peak_freq - 10.0) < 2.0
    True
    """
    if not isinstance(signal, (list, tuple)):
        raise TypeError("signal must be a list or tuple")
    if len(signal) == 0:
        raise ValueError("signal cannot be empty")
    if not isinstance(sampling_rate, (int, float)) or sampling_rate <= 0:
        raise ValueError("sampling_rate must be positive")
    if not isinstance(overlap, (int, float)) or not 0 <= overlap < 1:
        raise ValueError("overlap must be between 0 and 1")
    
    N = len(signal)
    
    # Determine segment length
    if nperseg is None:
        nperseg = max(256, N // 8)  # Default segment length
    nperseg = min(nperseg, N)
    
    # Calculate overlap in samples
    noverlap = int(nperseg * overlap)
    
    # Generate segments
    segments = []
    start = 0
    while start + nperseg <= N:
        segment = signal[start:start + nperseg]
        segments.append(segment)
        start += nperseg - noverlap
    
    if len(segments) == 0:
        # Single segment case
        segments = [signal[:nperseg]]
    
    # Compute PSD for each segment
    psds = []
    for segment in segments:
        # Apply FFT
        result = fourier_transform(segment, method='fft', window=window)
        
        # Compute power spectral density
        magnitude = result['magnitude']
        psd = [(mag ** 2) / (nperseg * sampling_rate) for mag in magnitude]
        psds.append(psd)
    
    # Average PSDs across segments
    if len(psds) > 1:
        avg_psd = []
        for i in range(len(psds[0])):
            avg_psd.append(sum(psd[i] for psd in psds) / len(psds))
    else:
        avg_psd = psds[0]
    
    # Generate frequency axis
    frequencies = [i * sampling_rate / nperseg for i in range(nperseg)]
    
    # Take only positive frequencies for real signals
    if all(isinstance(x, (int, float)) for x in signal):
        n_pos = nperseg // 2 + 1
        frequencies = frequencies[:n_pos]
        avg_psd = avg_psd[:n_pos]
        # Scale PSD (except DC and Nyquist)
        for i in range(1, len(avg_psd) - 1):
            avg_psd[i] *= 2
    
    # Find peak frequency
    max_idx = avg_psd.index(max(avg_psd[1:]))  # Skip DC component
    peak_frequency = frequencies[max_idx]
    
    # Calculate total power
    total_power = sum(avg_psd) * (sampling_rate / nperseg)
    
    return {
        'frequencies': frequencies,
        'psd': avg_psd,
        'peak_frequency': peak_frequency,
        'total_power': total_power,
        'frequency_resolution': sampling_rate / nperseg
    }


__all__ = ['fourier_transform', 'spectral_analysis']
