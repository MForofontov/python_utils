"""Unit tests for gather_with_timeout function."""
import asyncio

import pytest

from asyncio_functions.gather_with_timeout import gather_with_timeout


@pytest.mark.asyncio
async def test_gather_with_timeout_all_complete_before_timeout() -> None:
    """
    Test case 1: All awaitables complete before timeout.
    """
    # Arrange
    async def task1() -> int:
        await asyncio.sleep(0.01)
        return 1

    async def task2() -> int:
        await asyncio.sleep(0.02)
        return 2

    async def task3() -> int:
        await asyncio.sleep(0.01)
        return 3

    # Act
    results = await gather_with_timeout([task1(), task2(), task3()], timeout=1.0)

    # Assert
    assert results == [1, 2, 3]


@pytest.mark.asyncio
async def test_gather_with_timeout_timeout_reached() -> None:
    """
    Test case 2: Timeout is reached before tasks complete.
    """
    # Arrange
    async def slow_task() -> int:
        await asyncio.sleep(1.0)
        return 1

    async def fast_task() -> int:
        await asyncio.sleep(0.01)
        return 2

    # Act & Assert
    with pytest.raises(asyncio.TimeoutError):
        await gather_with_timeout([slow_task(), fast_task()], timeout=0.05)


@pytest.mark.asyncio
async def test_gather_with_timeout_empty_list() -> None:
    """
    Test case 3: Empty list of awaitables.
    """
    # Arrange
    awaitables: list[asyncio.Future[int]] = []

    # Act
    results = await gather_with_timeout(awaitables, timeout=1.0)

    # Assert
    assert results == []


@pytest.mark.asyncio
async def test_gather_with_timeout_single_awaitable() -> None:
    """
    Test case 4: Single awaitable completes successfully.
    """
    # Arrange
    async def single_task() -> str:
        await asyncio.sleep(0.01)
        return "complete"

    # Act
    results = await gather_with_timeout([single_task()], timeout=1.0)

    # Assert
    assert results == ["complete"]


@pytest.mark.asyncio
async def test_gather_with_timeout_very_short_timeout() -> None:
    """
    Test case 5: Very short timeout causes timeout error.
    """
    # Arrange
    async def task() -> int:
        await asyncio.sleep(0.1)
        return 42

    # Act & Assert
    with pytest.raises(asyncio.TimeoutError):
        await gather_with_timeout([task()], timeout=0.001)


@pytest.mark.asyncio
async def test_gather_with_timeout_mixed_completion_times() -> None:
    """
    Test case 6: Mixed task completion times, all within timeout.
    """
    # Arrange
    async def instant_task() -> int:
        return 1

    async def quick_task() -> int:
        await asyncio.sleep(0.01)
        return 2

    async def medium_task() -> int:
        await asyncio.sleep(0.02)
        return 3

    # Act
    results = await gather_with_timeout(
        [instant_task(), quick_task(), medium_task()], timeout=0.5
    )

    # Assert
    assert results == [1, 2, 3]
