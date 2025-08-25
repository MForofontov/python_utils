import pytest
import math
import cmath
from mathematical_functions.advanced.fourier_analysis import fourier_transform, spectral_analysis


def test_fourier_transform_dft_sine_wave() -> None:
    """
    Test case 1: Test DFT of pure sine wave.
    """
    # Create sine wave at 5 Hz
    N = 64
    sampling_rate = 64
    signal = [math.sin(2*math.pi*5*i/sampling_rate) for i in range(N)]
    
    result = fourier_transform(signal, method='dft', sampling_rate=sampling_rate)
    
    # Peak should be at 5 Hz
    frequencies = result['frequencies']
    magnitude = result['magnitude']
    
    # Find peak (excluding DC component)
    peak_idx = magnitude[1:N//2].index(max(magnitude[1:N//2])) + 1
    peak_freq = frequencies[peak_idx]
    
    assert abs(peak_freq - 5.0) < 1.0
    assert result['method_used'] == 'dft'
    assert len(result['transform']) == N


def test_fourier_transform_fft_cosine_wave() -> None:
    """
    Test case 2: Test FFT of pure cosine wave.
    """
    # Create cosine wave at 10 Hz
    N = 128
    sampling_rate = 128
    signal = [math.cos(2*math.pi*10*i/sampling_rate) for i in range(N)]
    
    result = fourier_transform(signal, method='fft', sampling_rate=sampling_rate)
    
    # Peak should be at 10 Hz
    frequencies = result['frequencies']
    magnitude = result['magnitude']
    
    peak_idx = magnitude[1:N//2].index(max(magnitude[1:N//2])) + 1
    peak_freq = frequencies[peak_idx]
    
    assert abs(peak_freq - 10.0) < 1.0
    assert result['method_used'] == 'fft'


def test_fourier_transform_dct_basic() -> None:
    """
    Test case 3: Test DCT transform.
    """
    signal = [1, 2, 3, 4, 3, 2, 1, 0]
    
    result = fourier_transform(signal, method='dct')
    
    assert result['method_used'] == 'dct'
    assert len(result['transform']) == len(signal)
    assert isinstance(result['transform'][0], complex)


def test_fourier_transform_dst_basic() -> None:
    """
    Test case 4: Test DST transform.
    """
    signal = [0, 1, 2, 3, 2, 1, 0]
    
    result = fourier_transform(signal, method='dst')
    
    assert result['method_used'] == 'dst'
    assert len(result['transform']) == len(signal)


def test_fourier_transform_inverse_dft() -> None:
    """
    Test case 5: Test inverse DFT.
    """
    original_signal = [1, 2, 3, 4]
    
    # Forward transform
    result_forward = fourier_transform(original_signal, method='dft')
    
    # Inverse transform
    result_inverse = fourier_transform(result_forward['transform'], 
                                     method='dft', inverse=True)
    
    # Should recover original signal (within numerical precision)
    for i in range(len(original_signal)):
        assert abs(result_inverse['transform'][i].real - original_signal[i]) < 1e-10


def test_fourier_transform_windowing_hann() -> None:
    """
    Test case 6: Test Hann windowing.
    """
    signal = [1] * 16  # Constant signal
    
    result = fourier_transform(signal, method='dft', window='hann')
    
    # Windowed signal should be different from original
    windowed = result['windowed_signal']
    assert windowed[0] != signal[0]  # Hann window tapers to zero at edges
    assert windowed[-1] != signal[-1]


def test_fourier_transform_windowing_hamming() -> None:
    """
    Test case 7: Test Hamming windowing.
    """
    signal = [1, 1, 1, 1, 1, 1, 1, 1]
    
    result = fourier_transform(signal, method='dft', window='hamming')
    
    windowed = result['windowed_signal']
    assert len(windowed) == len(signal)
    assert windowed != signal  # Should be different due to windowing


def test_fourier_transform_windowing_blackman() -> None:
    """
    Test case 8: Test Blackman windowing.
    """
    signal = list(range(8))
    
    result = fourier_transform(signal, method='dft', window='blackman')
    
    assert result['windowed_signal'] != signal
    assert len(result['windowed_signal']) == len(signal)


def test_fourier_transform_zero_padding() -> None:
    """
    Test case 9: Test zero padding.
    """
    signal = [1, 2, 3, 4]
    padded_length = 8
    
    result = fourier_transform(signal, method='dft', zero_padding=padded_length)
    
    assert len(result['transform']) == padded_length
    assert result['n_samples'] == padded_length


def test_fourier_transform_complex_input() -> None:
    """
    Test case 10: Test with complex input signal.
    """
    signal = [complex(1, 1), complex(2, -1), complex(0, 2), complex(-1, 0)]
    
    result = fourier_transform(signal, method='dft')
    
    assert len(result['transform']) == len(signal)
    assert all(isinstance(x, complex) for x in result['transform'])


def test_fourier_transform_return_structure() -> None:
    """
    Test case 11: Test return structure completeness.
    """
    signal = [1, 2, 3, 4]

    result = fourier_transform(signal, method='dft', sampling_rate=4)

    required_keys = ['transform', 'magnitude', 'phase', 'frequencies',
                     'method_used', 'n_samples', 'windowed_signal']
    for key in required_keys:
        assert key in result

    assert len(result['magnitude']) == len(signal)
    assert len(result['phase']) == len(signal)
    assert len(result['frequencies']) == len(signal)


def test_fourier_transform_empty_signal() -> None:
    """
    Test case 12: Test error with empty signal.
    """
    with pytest.raises(ValueError, match="signal cannot be empty"):
        fourier_transform([], method='dft')


def test_fourier_transform_invalid_method() -> None:
    """
    Test case 13: Test error with invalid method.
    """
    signal = [1, 2, 3, 4]
    
    with pytest.raises(ValueError, match="method must be one of"):
        fourier_transform(signal, method='invalid_method')


def test_fourier_transform_invalid_window() -> None:
    """
    Test case 14: Test error with invalid window.
    """
    signal = [1, 2, 3, 4]
    
    with pytest.raises(ValueError, match="window must be one of"):
        fourier_transform(signal, method='dft', window='invalid_window')


def test_fourier_transform_invalid_zero_padding() -> None:
    """
    Test case 15: Test error with invalid zero padding.
    """
    signal = [1, 2, 3, 4]
    
    with pytest.raises(ValueError, match="zero_padding must be integer"):
        fourier_transform(signal, method='dft', zero_padding=2)  # Less than signal length


def test_fourier_transform_type_errors() -> None:
    """
    Test case 16: Test type error handling.
    """
    with pytest.raises(TypeError, match="signal must be a list"):
        fourier_transform("not_a_list", method='dft')
    
    with pytest.raises(TypeError, match="signal elements must be numeric"):
        fourier_transform([1, "invalid", 3], method='dft')


def test_fourier_transform_invalid_sampling_rate() -> None:
    """
    Test case 17: Test error with invalid sampling rate.
    """
    signal = [1, 2, 3, 4]
    
    with pytest.raises(ValueError, match="sampling_rate must be positive"):
        fourier_transform(signal, method='dft', sampling_rate=0)


def test_spectral_analysis_basic() -> None:
    """
    Test case 18: Test basic spectral analysis.
    """
    # Create signal with known frequency
    N = 1000
    sampling_rate = 100
    signal = [math.sin(2*math.pi*10*i/sampling_rate) for i in range(N)]
    
    result = spectral_analysis(signal, sampling_rate)
    
    # Peak should be around 10 Hz
    peak_freq = result['peak_frequency']
    assert abs(peak_freq - 10.0) < 2.0
    
    assert 'frequencies' in result
    assert 'psd' in result
    assert 'total_power' in result


def test_spectral_analysis_custom_parameters() -> None:
    """
    Test case 19: Test spectral analysis with custom parameters.
    """
    signal = [math.cos(2*math.pi*5*i/50) for i in range(500)]
    
    result = spectral_analysis(signal, sampling_rate=50, window='hamming',
                             nperseg=100, overlap=0.75)

    assert isinstance(result['peak_frequency'], (int, float))
    assert isinstance(result['total_power'], (int, float))
    assert len(result['frequencies']) > 0


def test_spectral_analysis_noisy_signal() -> None:
    """
    Test case 20: Test spectral analysis with noisy signal.
    """
    import random
    
    # Create noisy sine wave
    N = 1000
    sampling_rate = 100
    signal = [math.sin(2*math.pi*15*i/sampling_rate) + 0.1*random.gauss(0, 1) 
              for i in range(N)]
    
    result = spectral_analysis(signal, sampling_rate)
    
    # Should still detect peak around 15 Hz despite noise
    peak_freq = result['peak_frequency']
    assert abs(peak_freq - 15.0) < 3.0


def test_spectral_analysis_multiple_frequencies() -> None:
    """
    Test case 21: Test spectral analysis with multiple frequency components.
    """
    N = 2000
    sampling_rate = 200
    signal = [math.sin(2*math.pi*10*i/sampling_rate) + 
              0.5*math.sin(2*math.pi*25*i/sampling_rate) for i in range(N)]
    
    result = spectral_analysis(signal, sampling_rate)
    
    # Should detect dominant frequency (10 Hz has higher amplitude)
    peak_freq = result['peak_frequency']
    assert abs(peak_freq - 10.0) < 2.0 or abs(peak_freq - 25.0) < 2.0


def test_spectral_analysis_invalid_input() -> None:
    """
    Test case 22: Test spectral analysis error handling.
    """
    with pytest.raises(TypeError, match="signal must be a list"):
        spectral_analysis("not_a_list", 100)

    with pytest.raises(ValueError, match="signal cannot be empty"):
        spectral_analysis([], 100)

    with pytest.raises(ValueError, match="sampling_rate must be positive"):
        spectral_analysis([1, 2, 3], 0)

    with pytest.raises(ValueError, match="overlap must be between 0 and 1"):
        spectral_analysis([1, 2, 3], 100, overlap=1.5)
