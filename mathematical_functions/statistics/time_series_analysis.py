"""Perform time series analysis with trend detection and forecasting."""

from typing import Union, List, Dict, Tuple, Optional
import math


def time_series_analysis(data: list[Union[int, float]], 
                        periods: Optional[int] = None,
                        forecast_steps: int = 5,
                        confidence_level: float = 0.95) -> Dict[str, Union[List[float], float, str, bool]]:
    """
    Perform comprehensive time series analysis with trend detection and forecasting.

    Analyzes time series data for trends, seasonality, and provides forecasts using
    multiple methods including linear trend, moving averages, and exponential smoothing.

    Parameters
    ----------
    data : list[int | float]
        Time series data values in chronological order.
    periods : int, optional
        Number of periods for seasonal analysis. If None, attempts auto-detection.
    forecast_steps : int, optional
        Number of future periods to forecast. Default 5.
    confidence_level : float, optional
        Confidence level for forecast intervals. Default 0.95.

    Returns
    -------
    dict[str, Union[List[float], float, str, bool]]
        Dictionary containing:
        - 'trend_direction': 'increasing', 'decreasing', or 'no_trend'
        - 'trend_strength': Float indicating strength of trend
        - 'trend_p_value': Statistical significance of trend
        - 'seasonal_detected': Boolean indicating seasonality presence
        - 'seasonal_period': Detected or specified seasonal period
        - 'forecasts': List of forecasted values
        - 'forecast_intervals': List of (lower, upper) confidence intervals
        - 'residuals': List of residuals from trend line
        - 'r_squared': Goodness of fit for trend
        - 'stationarity_test': Results of stationarity testing
        - 'method_used': Primary forecasting method used

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If data validation fails.

    Examples
    --------
    >>> # Trending data
    >>> data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> result = time_series_analysis(data, forecast_steps=3)
    >>> result['trend_direction']
    'increasing'
    >>> len(result['forecasts'])
    3
    """
    # Input validation
    if not isinstance(data, list):
        raise TypeError("data must be a list")
    if periods is not None and not isinstance(periods, int):
        raise TypeError("periods must be an integer or None")
    if not isinstance(forecast_steps, int):
        raise TypeError("forecast_steps must be an integer")
    if not isinstance(confidence_level, (int, float)):
        raise TypeError("confidence_level must be numeric")
    
    if len(data) < 4:
        raise ValueError("need at least 4 data points for time series analysis")
    if forecast_steps < 1:
        raise ValueError("forecast_steps must be at least 1")
    if periods is not None and periods < 2:
        raise ValueError("periods must be at least 2")
    if not (0 < confidence_level < 1):
        raise ValueError("confidence_level must be between 0 and 1")
    
    if not all(isinstance(val, (int, float)) for val in data):
        raise TypeError("all data values must be numeric")
    
    n = len(data)
    time_points = list(range(n))
    
    # Trend analysis using linear regression
    trend_results = _analyze_trend(data, time_points)
    
    # Seasonality detection
    if periods is None:
        periods = _detect_seasonality(data)
    
    seasonal_results = _analyze_seasonality(data, periods) if periods else {
        'seasonal_detected': False, 
        'seasonal_period': None,
        'seasonal_component': [0] * n
    }
    
    # Stationarity testing (simplified Augmented Dickey-Fuller test)
    stationarity_results = _test_stationarity(data)
    
    # Calculate residuals after removing trend and seasonality
    trend_line = [trend_results['intercept'] + trend_results['slope'] * t for t in time_points]
    seasonal_component = seasonal_results.get('seasonal_component', [0] * n)
    
    residuals = []
    for i in range(n):
        residual = data[i] - trend_line[i] - seasonal_component[i]
        residuals.append(residual)
    
    # Choose forecasting method based on data characteristics
    if abs(trend_results['slope']) > 0.1 and trend_results['p_value'] < 0.05:
        # Strong trend detected - use linear trend forecasting
        forecasts, intervals = _linear_trend_forecast(
            data, trend_results, forecast_steps, confidence_level
        )
        method_used = "linear_trend"
    elif seasonal_results['seasonal_detected']:
        # Seasonality detected - use seasonal naive or decomposition
        forecasts, intervals = _seasonal_forecast(
            data, seasonal_results, forecast_steps, confidence_level
        )
        method_used = "seasonal"
    else:
        # No strong patterns - use exponential smoothing
        forecasts, intervals = _exponential_smoothing_forecast(
            data, forecast_steps, confidence_level
        )
        method_used = "exponential_smoothing"
    
    return {
        'trend_direction': trend_results['direction'],
        'trend_strength': abs(trend_results['slope']),
        'trend_p_value': trend_results['p_value'],
        'seasonal_detected': seasonal_results['seasonal_detected'],
        'seasonal_period': seasonal_results['seasonal_period'],
        'forecasts': forecasts,
        'forecast_intervals': intervals,
        'residuals': residuals,
        'r_squared': trend_results['r_squared'],
        'stationarity_test': stationarity_results,
        'method_used': method_used
    }


def _analyze_trend(data: List[float], time_points: List[int]) -> Dict[str, Union[float, str]]:
    """Analyze linear trend in time series data."""
    n = len(data)
    
    # Linear regression for trend
    sum_t = sum(time_points)
    sum_y = sum(data)
    sum_t2 = sum(t ** 2 for t in time_points)
    sum_ty = sum(time_points[i] * data[i] for i in range(n))
    
    # Calculate slope and intercept
    denominator = n * sum_t2 - sum_t ** 2
    if denominator == 0:
        slope = 0
        intercept = sum_y / n
    else:
        slope = (n * sum_ty - sum_t * sum_y) / denominator
        intercept = (sum_y - slope * sum_t) / n
    
    # Calculate R-squared
    y_mean = sum_y / n
    y_pred = [intercept + slope * t for t in time_points]
    
    ss_res = sum((data[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y - y_mean) ** 2 for y in data)
    
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
    
    # Statistical significance of slope
    if n > 2 and denominator > 0:
        mse = ss_res / (n - 2)
        se_slope = math.sqrt(mse / (sum_t2 - sum_t ** 2 / n))
        t_stat = slope / se_slope if se_slope > 0 else 0
        # Approximate p-value for t-distribution
        p_value = 2 * (1 - _standard_normal_cdf(abs(t_stat))) if abs(t_stat) < 10 else 0.0
    else:
        p_value = 1.0
    
    # Determine trend direction
    if p_value < 0.05:
        direction = 'increasing' if slope > 0 else 'decreasing'
    else:
        direction = 'no_trend'
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'p_value': p_value,
        'direction': direction
    }


def _detect_seasonality(data: List[float], max_period: int = None) -> Optional[int]:
    """Detect seasonal patterns using autocorrelation."""
    n = len(data)
    if max_period is None:
        max_period = min(n // 3, 12)  # Don't search beyond n/3 or 12 periods
    
    if max_period < 2:
        return None
    
    # Calculate autocorrelations for different lags
    best_period = None
    max_autocorr = 0
    
    for period in range(2, max_period + 1):
        if n < period * 2:
            break
            
        # Calculate autocorrelation at this lag
        autocorr = _calculate_autocorrelation(data, period)
        
        # Look for strong positive autocorrelation
        if autocorr > max_autocorr and autocorr > 0.3:
            max_autocorr = autocorr
            best_period = period
    
    return best_period if max_autocorr > 0.5 else None


def _calculate_autocorrelation(data: List[float], lag: int) -> float:
    """Calculate autocorrelation at specified lag."""
    n = len(data)
    if lag >= n:
        return 0.0
    
    mean_val = sum(data) / n
    
    # Calculate covariance at lag
    numerator = sum((data[i] - mean_val) * (data[i + lag] - mean_val) 
                   for i in range(n - lag))
    
    # Calculate variance
    denominator = sum((x - mean_val) ** 2 for x in data)
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def _analyze_seasonality(data: List[float], period: int) -> Dict[str, Union[bool, int, List[float]]]:
    """Analyze seasonal patterns in the data."""
    n = len(data)
    
    if period >= n:
        return {'seasonal_detected': False, 'seasonal_period': None, 'seasonal_component': [0] * n}
    
    # Calculate seasonal averages
    seasonal_sums = [0.0] * period
    seasonal_counts = [0] * period
    
    for i, value in enumerate(data):
        season_index = i % period
        seasonal_sums[season_index] += value
        seasonal_counts[season_index] += 1
    
    # Calculate seasonal means
    seasonal_means = []
    overall_mean = sum(data) / n
    
    for i in range(period):
        if seasonal_counts[i] > 0:
            seasonal_mean = seasonal_sums[i] / seasonal_counts[i]
            seasonal_means.append(seasonal_mean - overall_mean)
        else:
            seasonal_means.append(0.0)
    
    # Create seasonal component for all data points
    seasonal_component = []
    for i in range(n):
        season_index = i % period
        seasonal_component.append(seasonal_means[season_index])
    
    # Test for significant seasonality
    seasonal_variance = sum(x ** 2 for x in seasonal_means) / period
    is_seasonal = seasonal_variance > (sum((x - overall_mean) ** 2 for x in data) / n) * 0.1
    
    return {
        'seasonal_detected': is_seasonal,
        'seasonal_period': period,
        'seasonal_component': seasonal_component
    }


def _test_stationarity(data: List[float]) -> Dict[str, Union[float, bool, str]]:
    """Simplified stationarity test (Augmented Dickey-Fuller approximation)."""
    n = len(data)
    
    # Calculate first differences
    diffs = [data[i] - data[i-1] for i in range(1, n)]
    
    # Simple mean reversion test
    lagged_values = data[:-1]
    diff_mean = sum(diffs) / len(diffs)
    
    # Calculate correlation between lagged values and differences
    if len(lagged_values) > 1:
        correlation = _pearson_correlation(lagged_values, diffs)
        test_statistic = correlation * math.sqrt((len(diffs) - 2) / (1 - correlation ** 2))
        
        # Critical values approximation for stationarity
        critical_value = -1.645  # Simplified 5% critical value
        is_stationary = test_statistic < critical_value
        
        return {
            'test_statistic': test_statistic,
            'critical_value': critical_value,
            'is_stationary': is_stationary,
            'interpretation': 'stationary' if is_stationary else 'non-stationary'
        }
    else:
        return {
            'test_statistic': 0.0,
            'critical_value': -1.645,
            'is_stationary': False,
            'interpretation': 'insufficient_data'
        }


def _linear_trend_forecast(data: List[float], trend_results: Dict, 
                         forecast_steps: int, confidence_level: float) -> Tuple[List[float], List[Tuple[float, float]]]:
    """Generate forecasts using linear trend extrapolation."""
    n = len(data)
    slope = trend_results['slope']
    intercept = trend_results['intercept']
    
    # Calculate residual standard error
    y_pred = [intercept + slope * t for t in range(n)]
    residuals = [data[i] - y_pred[i] for i in range(n)]
    mse = sum(r ** 2 for r in residuals) / max(1, n - 2)
    std_error = math.sqrt(mse)
    
    # Generate forecasts
    forecasts = []
    intervals = []
    
    alpha = 1 - confidence_level
    z_critical = _inverse_normal_cdf(1 - alpha / 2)
    
    for step in range(1, forecast_steps + 1):
        future_time = n + step - 1
        forecast = intercept + slope * future_time
        forecasts.append(forecast)
        
        # Prediction interval (simplified)
        margin = z_critical * std_error * math.sqrt(1 + 1/n + (future_time - (n-1)/2)**2 / sum((t - (n-1)/2)**2 for t in range(n)))
        intervals.append((forecast - margin, forecast + margin))
    
    return forecasts, intervals


def _seasonal_forecast(data: List[float], seasonal_results: Dict,
                      forecast_steps: int, confidence_level: float) -> Tuple[List[float], List[Tuple[float, float]]]:
    """Generate forecasts using seasonal patterns."""
    n = len(data)
    period = seasonal_results['seasonal_period']
    seasonal_component = seasonal_results['seasonal_component']
    
    # Use recent trend + seasonal pattern
    recent_data = data[-period:] if len(data) >= period else data
    base_level = sum(recent_data) / len(recent_data)
    
    # Estimate forecast error
    residuals = [data[i] - seasonal_component[i] - base_level for i in range(n)]
    std_error = math.sqrt(sum(r ** 2 for r in residuals) / max(1, n - 1))
    
    forecasts = []
    intervals = []
    
    alpha = 1 - confidence_level
    z_critical = _inverse_normal_cdf(1 - alpha / 2)
    
    for step in range(1, forecast_steps + 1):
        season_index = (n + step - 1) % period
        seasonal_adj = seasonal_component[season_index] if season_index < len(seasonal_component) else 0
        
        forecast = base_level + seasonal_adj
        forecasts.append(forecast)
        
        margin = z_critical * std_error
        intervals.append((forecast - margin, forecast + margin))
    
    return forecasts, intervals


def _exponential_smoothing_forecast(data: List[float], forecast_steps: int, 
                                  confidence_level: float) -> Tuple[List[float], List[Tuple[float, float]]]:
    """Generate forecasts using simple exponential smoothing."""
    if len(data) == 0:
        return [], []
    
    # Simple exponential smoothing with alpha = 0.3
    alpha = 0.3
    smoothed = [data[0]]
    
    for i in range(1, len(data)):
        smoothed.append(alpha * data[i] + (1 - alpha) * smoothed[i-1])
    
    # Calculate forecast errors
    errors = [data[i] - smoothed[i] for i in range(len(data))]
    mse = sum(e ** 2 for e in errors) / len(errors)
    std_error = math.sqrt(mse)
    
    # Generate forecasts (constant level)
    last_smooth = smoothed[-1]
    forecasts = [last_smooth] * forecast_steps
    
    # Prediction intervals
    alpha_conf = 1 - confidence_level
    z_critical = _inverse_normal_cdf(1 - alpha_conf / 2)
    
    intervals = []
    for step in range(1, forecast_steps + 1):
        # Error grows with forecast horizon
        margin = z_critical * std_error * math.sqrt(step)
        intervals.append((last_smooth - margin, last_smooth + margin))
    
    return forecasts, intervals


def _pearson_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient."""
    n = len(x)
    if n != len(y) or n == 0:
        return 0.0
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    return numerator / denominator if denominator > 0 else 0.0


def _standard_normal_cdf(z: float) -> float:
    """Approximate cumulative distribution function of standard normal."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def _inverse_normal_cdf(p: float) -> float:
    """Approximate inverse of standard normal CDF."""
    if p <= 0.5:
        return -_inverse_normal_cdf(1 - p)
    
    t = math.sqrt(-2 * math.log(1 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    
    return t - (c0 + c1 * t + c2 * t * t) / (1 + d1 * t + d2 * t * t + d3 * t * t * t)


__all__ = ['time_series_analysis']
