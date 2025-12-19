import time

import pytest
from circuit_breaker_functions.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_normal_operation() -> None:
    """
    Test case 1: Normal operation with successful calls.
    """
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1.0)

    def success_func() -> str:
        return "success"

    result = cb.call(success_func)

    assert result == "success"
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


def test_circuit_breaker_multiple_successes() -> None:
    """
    Test case 2: Multiple successful calls keep circuit closed.
    """
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1.0)

    def success_func() -> str:
        return "ok"

    for _ in range(5):
        result = cb.call(success_func)
        assert result == "ok"

    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


def test_circuit_breaker_with_args_and_kwargs() -> None:
    """
    Test case 3: Circuit breaker with function arguments.
    """
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1.0)

    def add_numbers(a: int, b: int, c: int = 0) -> int:
        return a + b + c

    result = cb.call(add_numbers, 1, 2, c=3)
    assert result == 6


def test_circuit_breaker_edge_case_opens_after_threshold() -> None:
    """
    Test case 4: Circuit opens after reaching failure threshold.
    """
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1.0)

    def failing_func() -> None:
        raise ValueError("Service unavailable")

    # Trigger failures
    for i in range(3):
        with pytest.raises(ValueError):
            cb.call(failing_func)
        if i < 2:
            assert cb.state == CircuitState.CLOSED

    assert cb.state == CircuitState.OPEN
    assert cb.failure_count == 0  # Reset when circuit opens


def test_circuit_breaker_edge_case_rejects_when_open() -> None:
    """
    Test case 5: Circuit rejects calls when open.
    """
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1.0)

    def failing_func() -> None:
        raise RuntimeError("Error")

    # Open the circuit
    for _ in range(2):
        with pytest.raises(RuntimeError):
            cb.call(failing_func)

    assert cb.state == CircuitState.OPEN

    # Should raise Exception immediately without calling function
    with pytest.raises(Exception, match="Circuit breaker is OPEN"):
        cb.call(lambda: "should not execute")


def test_circuit_breaker_edge_case_half_open_after_timeout() -> None:
    """
    Test case 6: Circuit transitions to half-open after recovery timeout.
    """
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    def failing_func() -> None:
        raise ValueError("Error")

    # Open the circuit
    for _ in range(2):
        with pytest.raises(ValueError):
            cb.call(failing_func)

    assert cb.state == CircuitState.OPEN

    # Wait for recovery timeout
    time.sleep(0.15)

    # Next call should transition to half-open and succeed
    def success_func() -> str:
        return "recovered"

    result = cb.call(success_func)
    assert result == "recovered"
    assert cb.state == CircuitState.HALF_OPEN


def test_circuit_breaker_edge_case_closes_after_success_threshold() -> None:
    """
    Test case 7: Circuit closes after success threshold in half-open state.
    """
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1, success_threshold=2)

    def failing_func() -> None:
        raise ValueError("Error")

    # Open the circuit
    for _ in range(2):
        with pytest.raises(ValueError):
            cb.call(failing_func)

    time.sleep(0.15)

    # Transition to half-open and succeed
    def success_func() -> str:
        return "ok"

    result1 = cb.call(success_func)
    assert result1 == "ok"
    assert cb.state == CircuitState.HALF_OPEN

    result2 = cb.call(success_func)
    assert result2 == "ok"
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


def test_circuit_breaker_edge_case_reopens_on_failure_in_half_open() -> None:
    """
    Test case 8: Circuit reopens on failure in half-open state.
    """
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    def failing_func() -> None:
        raise ValueError("Error")

    # Open the circuit
    for _ in range(2):
        with pytest.raises(ValueError):
            cb.call(failing_func)

    time.sleep(0.15)

    # Transition to half-open happens on next call

    # Fail again - should reopen circuit
    with pytest.raises(ValueError):
        cb.call(failing_func)

    assert cb.state == CircuitState.OPEN


def test_circuit_breaker_edge_case_reset() -> None:
    """
    Test case 9: Reset functionality.
    """
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1.0)

    def failing_func() -> None:
        raise ValueError("Error")

    # Open the circuit
    for _ in range(2):
        with pytest.raises(ValueError):
            cb.call(failing_func)

    assert cb.state == CircuitState.OPEN

    # Reset
    cb.reset()

    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0
    assert cb.last_failure_time is None


def test_circuit_breaker_type_error_invalid_failure_threshold() -> None:
    """
    Test case 10: TypeError for invalid failure threshold.
    """
    with pytest.raises(TypeError, match="failure_threshold must be an integer"):
        CircuitBreaker(failure_threshold="3", recovery_timeout=1.0)  # type: ignore[arg-type]


def test_circuit_breaker_value_error_negative_failure_threshold() -> None:
    """
    Test case 11: ValueError for negative failure threshold.
    """
    with pytest.raises(ValueError, match="failure_threshold must be positive"):
        CircuitBreaker(failure_threshold=0, recovery_timeout=1.0)


def test_circuit_breaker_type_error_invalid_recovery_timeout() -> None:
    """
    Test case 12: TypeError for invalid recovery timeout.
    """
    with pytest.raises(TypeError, match="recovery_timeout must be a number"):
        CircuitBreaker(failure_threshold=3, recovery_timeout="1.0")  # type: ignore[arg-type]


def test_circuit_breaker_value_error_negative_recovery_timeout() -> None:
    """
    Test case 13: ValueError for negative recovery timeout.
    """
    with pytest.raises(ValueError, match="recovery_timeout must be positive"):
        CircuitBreaker(failure_threshold=3, recovery_timeout=-1.0)


def test_circuit_breaker_type_error_invalid_success_threshold() -> None:
    """
    Test case 14: TypeError for invalid success threshold.
    """
    with pytest.raises(TypeError, match="success_threshold must be an integer"):
        CircuitBreaker(failure_threshold=3, recovery_timeout=1.0, success_threshold=1.5)  # type: ignore[arg-type]


def test_circuit_breaker_value_error_zero_success_threshold() -> None:
    """
    Test case 15: ValueError for zero success threshold.
    """
    with pytest.raises(ValueError, match="success_threshold must be positive"):
        CircuitBreaker(failure_threshold=3, recovery_timeout=1.0, success_threshold=0)


def test_circuit_breaker_type_error_non_callable() -> None:
    """
    Test case 16: TypeError for non-callable function.
    """
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1.0)

    with pytest.raises(TypeError, match="func must be callable"):
        cb.call("not_a_function")  # type: ignore[arg-type]
