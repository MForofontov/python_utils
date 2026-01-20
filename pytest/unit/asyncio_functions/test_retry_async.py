import asyncio

import pytest

try:
    import aiohttp
    from python_utils.asyncio_functions.retry_async import retry_async
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    aiohttp = None  # type: ignore
    retry_async = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.asyncio_functions,
    pytest.mark.skipif(not AIOHTTP_AVAILABLE, reason="aiohttp not installed"),
]


@pytest.mark.asyncio
async def test_retry_async_succeeds_first_try() -> None:
    """
    Test case 1: Function succeeds on first attempt.
    """
    # Arrange
    call_count = []

    async def successful_task() -> int:
        call_count.append(1)
        return 42

    # Act
    result = await retry_async(successful_task, retries=3, delay=0.01)

    # Assert
    assert result == 42
    assert len(call_count) == 1


@pytest.mark.asyncio
async def test_retry_async_succeeds_after_failures() -> None:
    """
    Test case 2: Function fails initially but succeeds on retry.
    """
    # Arrange
    call_count = []

    async def flaky_task() -> str:
        call_count.append(1)
        if len(call_count) < 3:
            raise ValueError("Temporary failure")
        return "success"

    # Act
    result = await retry_async(flaky_task, retries=5, delay=0.01)

    # Assert
    assert result == "success"
    assert len(call_count) == 3


@pytest.mark.asyncio
async def test_retry_async_single_retry() -> None:
    """
    Test case 3: Single retry attempt.
    """
    # Arrange
    call_count = []

    async def task() -> int:
        call_count.append(1)
        if len(call_count) == 1:
            raise ValueError("First attempt fails")
        return 100

    # Act
    result = await retry_async(task, retries=2, delay=0.01)

    # Assert
    assert result == 100
    assert len(call_count) == 2


@pytest.mark.asyncio
async def test_retry_async_different_exception_types() -> None:
    """
    Test case 4: Different exception types are handled.
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
    result = await retry_async(task_with_different_errors, retries=5, delay=0.01)

    # Assert
    assert result == "recovered"
    assert len(call_count) == 3


@pytest.mark.asyncio
async def test_retry_async_fails_all_retries() -> None:
    """
    Test case 5: Function fails on all retry attempts.
    """
    # Arrange
    call_count = []

    async def always_failing_task() -> int:
        call_count.append(1)
        raise ValueError("Permanent failure")

    # Act & Assert
    with pytest.raises(ValueError, match="Permanent failure"):
        await retry_async(always_failing_task, retries=3, delay=0.01)

    assert len(call_count) == 3


@pytest.mark.asyncio
async def test_retry_async_delay_between_retries() -> None:
    """
    Test case 6: Verify delay is applied between retries.
    """
    # Arrange
    call_times = []

    async def failing_task() -> None:
        call_times.append(asyncio.get_event_loop().time())
        raise ValueError("Fail")

    # Act & Assert
    with pytest.raises(ValueError):
        await retry_async(failing_task, retries=3, delay=0.05)

    # Verify timing
    assert len(call_times) == 3
    if len(call_times) >= 2:
        # Check delay between first and second call
        delay = call_times[1] - call_times[0]
        assert 0.04 <= delay <= 0.07
