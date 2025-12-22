"""
Unit tests for execute_with_retry function.
"""

import sqlite3
import time

import pytest

from database_functions import execute_with_retry


def test_execute_with_retry_successful_first_attempt() -> None:
    """
    Test case 1: Successful execution on first attempt.
    """
    # Arrange
    def successful_query():
        return [1, 2, 3]
    
    # Act
    result = execute_with_retry(successful_query, max_retries=3)
    
    # Assert
    assert result == [1, 2, 3]


def test_execute_with_retry_success_after_failures() -> None:
    """
    Test case 2: Success after some retries.
    """
    # Arrange
    attempt_count = [0]
    
    def flaky_query():
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise sqlite3.OperationalError("database is locked")
        return "success"
    
    # Act
    result = execute_with_retry(
        flaky_query,
        max_retries=3,
        retry_delay=0.01,
        retriable_exceptions=(sqlite3.OperationalError,)
    )
    
    # Assert
    assert result == "success"
    assert attempt_count[0] == 3


def test_execute_with_retry_max_retries_exceeded() -> None:
    """
    Test case 3: Raises exception after max retries exceeded.
    """
    # Arrange
    def failing_query():
        raise sqlite3.OperationalError("database is locked")
    
    # Act & Assert
    with pytest.raises(sqlite3.OperationalError):
        execute_with_retry(
            failing_query,
            max_retries=2,
            retry_delay=0.01,
            retriable_exceptions=(sqlite3.OperationalError,)
        )


def test_execute_with_retry_non_retriable_exception() -> None:
    """
    Test case 4: Non-retriable exceptions are raised immediately.
    """
    # Arrange
    attempt_count = [0]
    
    def query_with_integrity_error():
        attempt_count[0] += 1
        raise sqlite3.IntegrityError("constraint violation")
    
    # Act & Assert
    with pytest.raises(sqlite3.IntegrityError):
        execute_with_retry(
            query_with_integrity_error,
            max_retries=3,
            retry_delay=0.01,
            retriable_exceptions=(sqlite3.OperationalError,)
        )
    
    # Should only try once
    assert attempt_count[0] == 1


def test_execute_with_retry_exponential_backoff() -> None:
    """
    Test case 5: Exponential backoff delays between retries.
    """
    # Arrange
    attempt_count = [0]
    
    def query():
        attempt_count[0] += 1
        if attempt_count[0] < 2:
            raise sqlite3.OperationalError("locked")
        return "success"
    
    start_time = time.time()
    
    # Act
    result = execute_with_retry(
        query,
        max_retries=2,
        retry_delay=0.1,
        backoff_multiplier=2.0,
        retriable_exceptions=(sqlite3.OperationalError,)
    )
    
    elapsed = time.time() - start_time
    
    # Assert
    assert result == "success"
    assert elapsed >= 0.1  # At least one retry with 0.1s delay


def test_execute_with_retry_with_real_database() -> None:
    """
    Test case 6: Works with real database operations.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    
    def query_func():
        return conn.execute("SELECT * FROM users").fetchall()
    
    # Act
    result = execute_with_retry(query_func, max_retries=1)
    
    # Assert
    assert len(result) == 1
    assert result[0] == (1, "Alice")
    
    conn.close()


def test_execute_with_retry_returns_values() -> None:
    """
    Test case 7: Correctly returns various types of values.
    """
    # Arrange
    def return_list():
        return [1, 2, 3]
    
    def return_dict():
        return {"key": "value"}
    
    # Act
    list_result = execute_with_retry(return_list, max_retries=1)
    dict_result = execute_with_retry(return_dict, max_retries=1)
    
    # Assert
    assert list_result == [1, 2, 3]
    assert dict_result == {"key": "value"}


def test_execute_with_retry_invalid_execute_func() -> None:
    """
    Test case 8: Non-callable execute_func raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError):
        execute_with_retry("not_callable", max_retries=1)


def test_execute_with_retry_invalid_max_retries() -> None:
    """
    Test case 9: Invalid max_retries raises ValueError.
    """
    # Arrange
    def query():
        return "result"
    
    # Act & Assert
    with pytest.raises(ValueError):
        execute_with_retry(query, max_retries=0)
    
    with pytest.raises(ValueError):
        execute_with_retry(query, max_retries=-1)


def test_execute_with_retry_invalid_retry_delay() -> None:
    """
    Test case 10: Invalid retry_delay raises ValueError.
    """
    # Arrange
    def query():
        return "result"
    
    # Act & Assert
    with pytest.raises(ValueError):
        execute_with_retry(query, max_retries=1, retry_delay=0)
    
    with pytest.raises(ValueError):
        execute_with_retry(query, max_retries=1, retry_delay=-1)


def test_execute_with_retry_invalid_backoff_multiplier() -> None:
    """
    Test case 11: Invalid backoff_multiplier raises ValueError.
    """
    # Arrange
    def query():
        return "result"
    
    # Act & Assert
    with pytest.raises(ValueError):
        execute_with_retry(query, max_retries=1, backoff_multiplier=0.5)
