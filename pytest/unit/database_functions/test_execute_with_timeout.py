"""
Unit tests for execute_with_timeout function.
"""

import sys
import time

import pytest

from database_functions import execute_with_timeout, QueryTimeoutError


@pytest.mark.skipif(sys.platform == "win32", reason="signal.alarm not available on Windows")
def test_execute_with_timeout_fast_execution() -> None:
    """
    Test case 1: Function completes quickly within timeout.
    """
    # Arrange
    def fast_function():
        return sum(range(100))
    
    # Act
    result = execute_with_timeout(fast_function, timeout_seconds=5.0)
    
    # Assert
    assert result == 4950


@pytest.mark.skipif(
    sys.platform in ("win32", "darwin"),
    reason="signal.alarm not reliable on Windows/macOS - doesn't interrupt Python code"
)
def test_execute_with_timeout_timeout_exceeded() -> None:
    """
    Test case 2: Raises QueryTimeoutError when timeout exceeded.
    """
    # Arrange - signal.alarm doesn't interrupt time.sleep, so we use a busy loop
    def slow_function():
        start = time.time()
        while time.time() - start < 2.0:
            pass  # Busy wait that can be interrupted
        return "should not reach"
    
    # Act & Assert
    with pytest.raises(QueryTimeoutError):
        execute_with_timeout(slow_function, timeout_seconds=0.5)


@pytest.mark.skipif(sys.platform == "win32", reason="signal.alarm not available on Windows")
def test_execute_with_timeout_with_computation() -> None:
    """
    Test case 3: Handles computational tasks correctly.
    """
    # Arrange
    def compute_factorial():
        result = 1
        for i in range(1, 21):
            result *= i
        return result
    
    # Act
    result = execute_with_timeout(compute_factorial, timeout_seconds=2.0)
    
    # Assert
    assert result == 2432902008176640000


@pytest.mark.skipif(sys.platform == "win32", reason="signal.alarm not available on Windows")
def test_execute_with_timeout_exception_during_execution() -> None:
    """
    Test case 4: Original exception is raised, not timeout.
    """
    # Arrange
    def failing_function():
        raise ValueError("Function error")
    
    # Act & Assert
    with pytest.raises(ValueError, match="Function error"):
        execute_with_timeout(failing_function, timeout_seconds=5.0)


@pytest.mark.skipif(sys.platform == "win32", reason="signal.alarm not available on Windows")
def test_execute_with_timeout_returns_values() -> None:
    """
    Test case 5: Correctly returns various types of values.
    """
    # Arrange
    def return_list():
        return [1, 2, 3, 4, 5]
    
    def return_dict():
        return {"key": "value", "number": 42}
    
    # Act
    list_result = execute_with_timeout(return_list, timeout_seconds=1.0)
    dict_result = execute_with_timeout(return_dict, timeout_seconds=1.0)
    
    # Assert
    assert list_result == [1, 2, 3, 4, 5]
    assert dict_result == {"key": "value", "number": 42}


@pytest.mark.skipif(sys.platform == "win32", reason="signal.alarm not available on Windows")
def test_execute_with_timeout_very_short_timeout() -> None:
    """
    Test case 6: Handles very short timeouts for instant functions.
    """
    # Arrange
    def instant_function():
        return 42
    
    # Act
    result = execute_with_timeout(instant_function, timeout_seconds=0.001)
    
    # Assert
    assert result == 42


def test_execute_with_timeout_invalid_execute_func() -> None:
    """
    Test case 7: Non-callable execute_func raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError):
        execute_with_timeout("not_callable", timeout_seconds=5.0)


def test_execute_with_timeout_invalid_timeout() -> None:
    """
    Test case 8: Invalid timeout values raise ValueError.
    """
    # Arrange
    def some_function():
        return "result"
    
    # Act & Assert
    with pytest.raises(ValueError):
        execute_with_timeout(some_function, timeout_seconds=0)
    
    with pytest.raises(ValueError):
        execute_with_timeout(some_function, timeout_seconds=-1)


def test_execute_with_timeout_invalid_timeout_type() -> None:
    """
    Test case 9: Non-numeric timeout raises TypeError.
    """
    # Arrange
    def some_function():
        return "result"
    
    # Act & Assert
    with pytest.raises(TypeError):
        execute_with_timeout(some_function, timeout_seconds="not_a_number")
