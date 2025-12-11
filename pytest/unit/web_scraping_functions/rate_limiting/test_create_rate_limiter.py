import pytest
import time
from web_scraping_functions.rate_limiting.create_rate_limiter import (
    create_rate_limiter,
)


def test_create_rate_limiter_case_1_basic_rate_limiting() -> None:
    """
    Test case 1: Basic rate limiting with wait method.
    """
    # Arrange
    limiter = create_rate_limiter(calls_per_second=10)
    
    # Act
    start_time = time.time()
    limiter.wait()
    limiter.wait()
    elapsed = time.time() - start_time
    
    # Assert
    assert elapsed >= 0.1  # At least 0.1 seconds between calls


def test_create_rate_limiter_case_2_multiple_waits() -> None:
    """
    Test case 2: Multiple wait calls respect rate limit.
    """
    # Arrange
    limiter = create_rate_limiter(calls_per_second=5)
    
    # Act
    start_time = time.time()
    for _ in range(3):
        limiter.wait()
    elapsed = time.time() - start_time
    
    # Assert
    assert elapsed >= 0.4  # At least 0.4 seconds for 3 calls at 5/sec


def test_create_rate_limiter_case_3_fast_rate() -> None:
    """
    Test case 3: Fast rate limiting (100 calls per second).
    """
    # Arrange
    limiter = create_rate_limiter(calls_per_second=100)
    
    # Act
    start_time = time.time()
    limiter.wait()
    limiter.wait()
    elapsed = time.time() - start_time
    
    # Assert
    assert elapsed >= 0.01  # At least 0.01 seconds between calls


def test_create_rate_limiter_case_4_slow_rate() -> None:
    """
    Test case 4: Slow rate limiting (1 call per second).
    """
    # Arrange
    limiter = create_rate_limiter(calls_per_second=1)
    
    # Act
    start_time = time.time()
    limiter.wait()
    limiter.wait()
    elapsed = time.time() - start_time
    
    # Assert
    assert elapsed >= 1.0  # At least 1 second between calls


def test_create_rate_limiter_case_5_rate_attribute() -> None:
    """
    Test case 5: Verify rate limiter has rate attribute.
    """
    # Arrange
    limiter = create_rate_limiter(calls_per_second=5)
    
    # Act & Assert
    assert hasattr(limiter, 'rate')
    assert limiter.rate == 5


def test_create_rate_limiter_case_6_type_error_calls_per_second() -> None:
    """
    Test case 6: TypeError for invalid calls_per_second type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="calls_per_second must be a number"):
        create_rate_limiter(calls_per_second="5")


def test_create_rate_limiter_case_7_value_error_zero_rate() -> None:
    """
    Test case 7: ValueError for zero calls_per_second.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="calls_per_second must be positive"):
        create_rate_limiter(calls_per_second=0)


def test_create_rate_limiter_case_8_value_error_negative_rate() -> None:
    """
    Test case 8: ValueError for negative calls_per_second.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="calls_per_second must be positive"):
        create_rate_limiter(calls_per_second=-5)


def test_create_rate_limiter_case_9_fractional_rate() -> None:
    """
    Test case 9: Support fractional calls per second.
    """
    # Arrange
    limiter = create_rate_limiter(calls_per_second=2.5)
    
    # Act
    start_time = time.time()
    limiter.wait()
    limiter.wait()
    elapsed = time.time() - start_time
    
    # Assert
    assert elapsed >= 0.4  # At least 0.4 seconds (1/2.5)
