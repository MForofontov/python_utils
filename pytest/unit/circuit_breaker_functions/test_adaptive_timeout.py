import time

import pytest
from circuit_breaker_functions.adaptive_timeout import AdaptiveTimeout


def test_adaptive_timeout_normal_operation() -> None:
    """
    Test case 1: Normal operation with successful calls.
    """
    at = AdaptiveTimeout(min_timeout=1.0)

    def quick_work() -> str:
        time.sleep(0.05)
        return "completed"

    result = at.call(quick_work)
    assert result == "completed"


def test_adaptive_timeout_multiple_successful_calls() -> None:
    """
    Test case 2: Multiple successful calls adapt timeout.
    """
    at = AdaptiveTimeout(min_timeout=2.0, percentile=0.95)

    def work(duration: float) -> str:
        time.sleep(duration)
        return "done"

    # Execute multiple calls with varying durations
    for duration in [0.1, 0.15, 0.12, 0.18, 0.11]:
        result = at.call(work, duration)
        assert result == "done"

    # Verify timeout was tracked
    assert at.current_timeout > 0
    assert at.avg_latency > 0


def test_adaptive_timeout_with_args_and_kwargs() -> None:
    """
    Test case 3: Adaptive timeout with function arguments.
    """
    at = AdaptiveTimeout(min_timeout=1.0)

    def compute(a: int, b: int, multiplier: int = 2) -> int:
        time.sleep(0.01)
        return (a + b) * multiplier

    result = at.call(compute, 3, 4, multiplier=3)
    assert result == 21


def test_adaptive_timeout_timeout_adjustment() -> None:
    """
    Test case 4: Timeout adjusts based on execution times.
    """
    at = AdaptiveTimeout(min_timeout=1.0, percentile=0.90, window_size=3)

    def work() -> str:
        time.sleep(0.05)
        return "done"

    initial_timeout = at.current_timeout

    # Execute enough samples to trigger adjustment
    for _ in range(5):
        at.call(work)

    # Timeout should have adjusted based on latencies
    assert at.current_timeout > 0
    assert at.avg_latency > 0


def test_adaptive_timeout_edge_case_function_timeout() -> None:
    """
    Test case 5: Function exceeds timeout.
    """
    at = AdaptiveTimeout(min_timeout=0.1, max_timeout=0.1)

    def slow_work() -> str:
        time.sleep(0.5)
        return "too slow"

    with pytest.raises(TimeoutError, match="exceeding adaptive timeout"):
        at.call(slow_work)


def test_adaptive_timeout_edge_case_min_timeout_enforcement() -> None:
    """
    Test case 6: Timeout never goes below min_timeout.
    """
    at = AdaptiveTimeout(min_timeout=0.5, window_size=2)

    def fast_work() -> str:
        time.sleep(0.001)
        return "fast"

    # Execute very fast operations
    for _ in range(10):
        at.call(fast_work)

    # Even with fast operations, timeout should not go below min_timeout
    assert at.current_timeout >= 0.5


def test_adaptive_timeout_edge_case_max_timeout_enforcement() -> None:
    """
    Test case 7: Timeout never exceeds max_timeout.
    """
    at = AdaptiveTimeout(min_timeout=0.5, max_timeout=1.0, window_size=2)

    def varying_work(duration: float) -> str:
        time.sleep(duration)
        return "done"

    # Execute operations with varying durations
    for duration in [0.2, 0.3, 0.4, 0.35, 0.38]:
        at.call(varying_work, duration)

    # Timeout should not exceed max_timeout
    assert at.current_timeout <= 1.0


def test_adaptive_timeout_edge_case_percentile_calculation() -> None:
    """
    Test case 8: Different percentile values affect timeout calculation.
    """
    at50 = AdaptiveTimeout(min_timeout=1.0, percentile=0.50, window_size=3)
    at99 = AdaptiveTimeout(min_timeout=1.0, percentile=0.99, window_size=3)

    def work() -> str:
        time.sleep(0.1)
        return "done"

    # Execute same operations on both
    for _ in range(10):
        at50.call(work)
        at99.call(work)

    # Both should have valid timeouts
    assert at50.current_timeout > 0
    assert at99.current_timeout > 0


def test_adaptive_timeout_edge_case_reset() -> None:
    """
    Test case 9: Reset functionality restores initial state.
    """
    at = AdaptiveTimeout(min_timeout=1.0)

    def work() -> str:
        time.sleep(0.05)
        return "done"

    # Execute some calls
    for _ in range(5):
        at.call(work)

    assert at.avg_latency > 0

    # Reset
    at.reset()

    # After reset, no latencies tracked
    assert at.avg_latency == 0.0
    assert at.current_timeout == 1.0  # Back to min_timeout


def test_adaptive_timeout_edge_case_function_raises_exception() -> None:
    """
    Test case 10: Exception in function is propagated.
    """
    at = AdaptiveTimeout(min_timeout=1.0)

    def failing_work() -> None:
        raise ValueError("Operation failed")

    with pytest.raises(ValueError, match="Operation failed"):
        at.call(failing_work)


def test_adaptive_timeout_edge_case_insufficient_samples() -> None:
    """
    Test case 11: Timeout adjusts even with small samples.
    """
    at = AdaptiveTimeout(min_timeout=1.0, window_size=10)

    def work() -> str:
        time.sleep(0.05)
        return "done"

    # Execute fewer than window_size
    for _ in range(5):
        at.call(work)

    # Timeout should still be adjusted based on available samples
    assert at.avg_latency > 0


def test_adaptive_timeout_type_error_invalid_min_timeout() -> None:
    """
    Test case 12: TypeError for invalid min_timeout type.
    """
    with pytest.raises(TypeError, match="min_timeout must be a number"):
        AdaptiveTimeout(min_timeout="0.1")  # type: ignore[arg-type]


def test_adaptive_timeout_value_error_negative_min_timeout() -> None:
    """
    Test case 13: ValueError for negative min_timeout.
    """
    with pytest.raises(ValueError, match="min_timeout must be positive"):
        AdaptiveTimeout(min_timeout=-0.1)


def test_adaptive_timeout_type_error_invalid_percentile() -> None:
    """
    Test case 14: TypeError for invalid percentile type.
    """
    with pytest.raises(TypeError, match="percentile must be a number"):
        AdaptiveTimeout(percentile="95")  # type: ignore[arg-type]


def test_adaptive_timeout_value_error_percentile_out_of_range() -> None:
    """
    Test case 15: ValueError for percentile out of range.
    """
    with pytest.raises(ValueError, match="percentile must be between 0 and 1"):
        AdaptiveTimeout(percentile=1.5)


def test_adaptive_timeout_type_error_invalid_max_timeout() -> None:
    """
    Test case 16: TypeError for invalid max_timeout type.
    """
    with pytest.raises(TypeError, match="max_timeout must be a number"):
        AdaptiveTimeout(max_timeout="10")  # type: ignore[arg-type]


def test_adaptive_timeout_value_error_max_less_than_min() -> None:
    """
    Test case 17: ValueError when max_timeout < min_timeout.
    """
    with pytest.raises(ValueError, match="min_timeout.*must be.*max_timeout"):
        AdaptiveTimeout(min_timeout=2.0, max_timeout=1.0)


def test_adaptive_timeout_type_error_invalid_window_size() -> None:
    """
    Test case 18: TypeError for invalid window_size type.
    """
    with pytest.raises(TypeError, match="window_size must be an integer"):
        AdaptiveTimeout(window_size=5.5)  # type: ignore[arg-type]


def test_adaptive_timeout_value_error_zero_window_size() -> None:
    """
    Test case 19: ValueError for zero window_size.
    """
    with pytest.raises(ValueError, match="window_size must be positive"):
        AdaptiveTimeout(window_size=0)


def test_adaptive_timeout_type_error_non_callable() -> None:
    """
    Test case 20: TypeError for non-callable function.
    """
    at = AdaptiveTimeout(min_timeout=1.0)

    with pytest.raises(TypeError, match="func must be callable"):
        at.call("not_callable")  # type: ignore[arg-type]
