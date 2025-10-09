"""Unit tests for async_retry_with_backoff function."""
import asyncio

import pytest

from asyncio_functions.async_retry_with_backoff import async_retry_with_backoff


@pytest.mark.asyncio
async def test_async_retry_with_backoff_succeeds_first_try() -> None:
    """
    Test case 1: Function succeeds on first attempt.
    """
    # Arrange
    call_count = []

    async def successful_task() -> int:
        call_count.append(1)
        return 42

    # Act
    result = await async_retry_with_backoff(
        successful_task, retries=3, initial_delay=0.01, backoff_factor=2
    )

    # Assert
    assert result == 42
    assert len(call_count) == 1


@pytest.mark.asyncio
async def test_async_retry_with_backoff_succeeds_after_retries() -> None:
    """
    Test case 2: Function fails initially but succeeds after retries.
    """
    # Arrange
    call_count = []

    async def flaky_task() -> str:
        call_count.append(1)
        if len(call_count) < 3:
            raise ValueError("Temporary failure")
        return "success"

    # Act
    result = await async_retry_with_backoff(
        flaky_task, retries=5, initial_delay=0.01, backoff_factor=2
    )

    # Assert
    assert result == "success"
    assert len(call_count) == 3


@pytest.mark.asyncio
async def test_async_retry_with_backoff_fails_all_retries() -> None:
    """
    Test case 3: Function fails on all retry attempts.
    """
    # Arrange
    call_count = []

    async def always_failing_task() -> int:
        call_count.append(1)
        raise ValueError("Permanent failure")

    # Act & Assert
    with pytest.raises(ValueError, match="Permanent failure"):
        await async_retry_with_backoff(
            always_failing_task, retries=3, initial_delay=0.01, backoff_factor=2
        )

    assert len(call_count) == 3


@pytest.mark.asyncio
async def test_async_retry_with_backoff_zero_retries() -> None:
    """
    Test case 4: Zero retries means single attempt.
    """
    # Arrange
    call_count = []

    async def task() -> int:
        call_count.append(1)
        return 100

    # Act
    result = await async_retry_with_backoff(
        task, retries=0, initial_delay=0.01, backoff_factor=2
    )

    # Assert
    assert result == 100
    assert len(call_count) == 1


@pytest.mark.asyncio
async def test_async_retry_with_backoff_exponential_backoff() -> None:
    """
    Test case 5: Verify exponential backoff delays are applied.
    """
    # Arrange
    call_times = []

    async def failing_task() -> None:
        call_times.append(asyncio.get_event_loop().time())
        raise ValueError("Fail")

    # Act & Assert
    with pytest.raises(ValueError):
        await async_retry_with_backoff(
            failing_task, retries=3, initial_delay=0.05, backoff_factor=2
        )

    # Verify backoff timing
    assert len(call_times) == 3
    if len(call_times) >= 2:
        # First delay should be ~0.05
        delay1 = call_times[1] - call_times[0]
        assert 0.04 <= delay1 <= 0.07

    if len(call_times) >= 3:
        # Second delay should be ~0.1 (0.05 * 2)
        delay2 = call_times[2] - call_times[1]
        assert 0.08 <= delay2 <= 0.12


@pytest.mark.asyncio
async def test_async_retry_with_backoff_different_exceptions() -> None:
    """
    Test case 6: Different exception types are handled.
    """
    # Arrange
    call_count = []

    async def task_with_different_errors() -> str:
        call_count.append(1)
        if len(call_count) == 1:
            raise ValueError("First error")
        elif len(call_count) == 2:
            raise RuntimeError("Second error")
        return "recovered"

    # Act
    result = await async_retry_with_backoff(
        task_with_different_errors, retries=5, initial_delay=0.01, backoff_factor=2
    )

    # Assert
    assert result == "recovered"
    assert len(call_count) == 3
