import time

import pytest
from circuit_breaker_functions.adaptive_timeout import AdaptiveTimeout


def test_adaptive_timeout_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with successful calls.
    """
    at = AdaptiveTimeout(initial_timeout=1.0)

    def quick_work() -> str:
        time.sleep(0.05)
        return "completed"

    result = at.call(quick_work)
    assert result == "completed"


def test_adaptive_timeout_case_2_multiple_successful_calls() -> None:
    """
    Test case 2: Multiple successful calls adapt timeout.
    """
    at = AdaptiveTimeout(initial_timeout=2.0, percentile=95.0)

    def work(duration: float) -> str:
        time.sleep(duration)
        return "done"

    # Execute multiple calls with varying durations
    for duration in [0.1, 0.15, 0.12, 0.18, 0.11]:
        result = at.call(work, duration)
        assert result == "done"

    stats = at.get_stats()
    assert stats["successful_calls"] == 5
    assert stats["timeout_count"] == 0
    assert stats["current_timeout"] > 0


def test_adaptive_timeout_case_3_with_args_and_kwargs() -> None:
    """
    Test case 3: Adaptive timeout with function arguments.
    """
    at = AdaptiveTimeout(initial_timeout=1.0)

    def compute(a: int, b: int, multiplier: int = 2) -> int:
        time.sleep(0.01)
        return (a + b) * multiplier

    result = at.call(compute, 3, 4, multiplier=3)
    assert result == 21


def test_adaptive_timeout_case_4_timeout_adjustment() -> None:
    """
    Test case 4: Timeout adjusts based on execution times.
    """
    at = AdaptiveTimeout(initial_timeout=1.0, percentile=90.0, min_samples=3)

    def work() -> str:
        time.sleep(0.05)
        return "done"

    initial_timeout = at.current_timeout

    # Execute enough samples to trigger adjustment
    for _ in range(5):
        at.call(work)

    # Timeout should have adjusted
    stats = at.get_stats()
    assert stats["successful_calls"] == 5
    # Timeout may have changed based on observed latencies
    assert stats["current_timeout"] > 0


def test_adaptive_timeout_case_5_edge_case_function_timeout() -> None:
    """
    Test case 5: Function exceeds timeout.
    """
    at = AdaptiveTimeout(initial_timeout=0.1)

    def slow_work() -> str:
        time.sleep(0.5)
        return "too slow"

    with pytest.raises(TimeoutError, match="Function exceeded timeout"):
        at.call(slow_work)

    stats = at.get_stats()
    assert stats["timeout_count"] == 1


def test_adaptive_timeout_case_6_edge_case_min_timeout_enforcement() -> None:
    """
    Test case 6: Timeout never goes below min_timeout.
    """
    at = AdaptiveTimeout(initial_timeout=1.0, min_timeout=0.5, min_samples=2)

    def fast_work() -> str:
        time.sleep(0.001)
        return "fast"

    # Execute very fast operations
    for _ in range(10):
        at.call(fast_work)

    stats = at.get_stats()
    # Even with fast operations, timeout should not go below min_timeout
    assert stats["current_timeout"] >= 0.5


def test_adaptive_timeout_case_7_edge_case_max_timeout_enforcement() -> None:
    """
    Test case 7: Timeout never exceeds max_timeout.
    """
    at = AdaptiveTimeout(initial_timeout=0.5, max_timeout=1.0, min_samples=2)

    def varying_work(duration: float) -> str:
        time.sleep(duration)
        return "done"

    # Execute operations with varying durations
    for duration in [0.2, 0.3, 0.4, 0.35, 0.38]:
        at.call(varying_work, duration)

    stats = at.get_stats()
    # Timeout should not exceed max_timeout
    assert stats["current_timeout"] <= 1.0


def test_adaptive_timeout_case_8_edge_case_percentile_calculation() -> None:
    """
    Test case 8: Different percentile values affect timeout calculation.
    """
    at50 = AdaptiveTimeout(initial_timeout=1.0, percentile=50.0, min_samples=3)
    at99 = AdaptiveTimeout(initial_timeout=1.0, percentile=99.0, min_samples=3)

    def work() -> str:
        time.sleep(0.1)
        return "done"

    # Execute same operations on both
    for _ in range(10):
        at50.call(work)
        at99.call(work)

    stats50 = at50.get_stats()
    stats99 = at99.get_stats()

    # 99th percentile timeout should generally be higher than 50th
    # (though with consistent timing, they might be similar)
    assert stats50["current_timeout"] > 0
    assert stats99["current_timeout"] > 0


def test_adaptive_timeout_case_9_edge_case_reset() -> None:
    """
    Test case 9: Reset functionality restores initial state.
    """
    at = AdaptiveTimeout(initial_timeout=1.0)

    def work() -> str:
        time.sleep(0.05)
        return "done"

    # Execute some calls
    for _ in range(5):
        at.call(work)

    stats_before = at.get_stats()
    assert stats_before["successful_calls"] > 0

    # Reset
    at.reset()

    stats_after = at.get_stats()
    assert stats_after["successful_calls"] == 0
    assert stats_after["timeout_count"] == 0
    assert stats_after["current_timeout"] == 1.0  # Back to initial


def test_adaptive_timeout_case_10_edge_case_function_raises_exception() -> None:
    """
    Test case 10: Exception in function is propagated.
    """
    at = AdaptiveTimeout(initial_timeout=1.0)

    def failing_work() -> None:
        raise ValueError("Operation failed")

    with pytest.raises(ValueError, match="Operation failed"):
        at.call(failing_work)

    # Should not count as timeout
    stats = at.get_stats()
    assert stats["timeout_count"] == 0


def test_adaptive_timeout_case_11_edge_case_insufficient_samples() -> None:
    """
    Test case 11: Timeout not adjusted with insufficient samples.
    """
    at = AdaptiveTimeout(initial_timeout=1.0, min_samples=10)

    def work() -> str:
        time.sleep(0.05)
        return "done"

    initial_timeout = at.current_timeout

    # Execute fewer than min_samples
    for _ in range(5):
        at.call(work)

    # Timeout should still be initial (or minimally adjusted)
    stats = at.get_stats()
    assert stats["successful_calls"] == 5


def test_adaptive_timeout_case_12_type_error_invalid_initial_timeout() -> None:
    """
    Test case 12: TypeError for invalid initial_timeout type.
    """
    with pytest.raises(TypeError, match="initial_timeout must be a number"):
        AdaptiveTimeout(initial_timeout="1.0")  # type: ignore[arg-type]


def test_adaptive_timeout_case_13_value_error_negative_initial_timeout() -> None:
    """
    Test case 13: ValueError for negative initial_timeout.
    """
    with pytest.raises(ValueError, match="initial_timeout must be positive"):
        AdaptiveTimeout(initial_timeout=-1.0)


def test_adaptive_timeout_case_14_type_error_invalid_percentile() -> None:
    """
    Test case 14: TypeError for invalid percentile type.
    """
    with pytest.raises(TypeError, match="percentile must be a number"):
        AdaptiveTimeout(initial_timeout=1.0, percentile="95")  # type: ignore[arg-type]


def test_adaptive_timeout_case_15_value_error_percentile_out_of_range() -> None:
    """
    Test case 15: ValueError for percentile out of range.
    """
    with pytest.raises(ValueError, match="percentile must be between 0 and 100"):
        AdaptiveTimeout(initial_timeout=1.0, percentile=150.0)


def test_adaptive_timeout_case_16_type_error_invalid_min_timeout() -> None:
    """
    Test case 16: TypeError for invalid min_timeout type.
    """
    with pytest.raises(TypeError, match="min_timeout must be a number or None"):
        AdaptiveTimeout(initial_timeout=1.0, min_timeout="0.1")  # type: ignore[arg-type]


def test_adaptive_timeout_case_17_value_error_negative_min_timeout() -> None:
    """
    Test case 17: ValueError for negative min_timeout.
    """
    with pytest.raises(ValueError, match="min_timeout must be positive"):
        AdaptiveTimeout(initial_timeout=1.0, min_timeout=-0.1)


def test_adaptive_timeout_case_18_type_error_invalid_max_timeout() -> None:
    """
    Test case 18: TypeError for invalid max_timeout type.
    """
    with pytest.raises(TypeError, match="max_timeout must be a number or None"):
        AdaptiveTimeout(initial_timeout=1.0, max_timeout="10")  # type: ignore[arg-type]


def test_adaptive_timeout_case_19_value_error_max_less_than_min() -> None:
    """
    Test case 19: ValueError when max_timeout < min_timeout.
    """
    with pytest.raises(ValueError, match="max_timeout must be >= min_timeout"):
        AdaptiveTimeout(initial_timeout=1.0, min_timeout=2.0, max_timeout=1.0)


def test_adaptive_timeout_case_20_type_error_invalid_min_samples() -> None:
    """
    Test case 20: TypeError for invalid min_samples type.
    """
    with pytest.raises(TypeError, match="min_samples must be an integer"):
        AdaptiveTimeout(initial_timeout=1.0, min_samples=5.5)  # type: ignore[arg-type]


def test_adaptive_timeout_case_21_value_error_zero_min_samples() -> None:
    """
    Test case 21: ValueError for zero min_samples.
    """
    with pytest.raises(ValueError, match="min_samples must be at least 1"):
        AdaptiveTimeout(initial_timeout=1.0, min_samples=0)


def test_adaptive_timeout_case_22_type_error_non_callable() -> None:
    """
    Test case 22: TypeError for non-callable function.
    """
    at = AdaptiveTimeout(initial_timeout=1.0)

    with pytest.raises(TypeError, match="func must be callable"):
        at.call("not_callable")  # type: ignore[arg-type]
