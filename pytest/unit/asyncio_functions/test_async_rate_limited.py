import asyncio
import time

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.asyncio_functions]
from python_utils.asyncio_functions.async_rate_limited import async_rate_limited


async def echo(value: int) -> int:
    await asyncio.sleep(0.01)
    return value


def generate_numbers():
    yield from range(3)


@pytest.mark.asyncio
async def test_async_rate_limited_success() -> None:
    """Test case 1: Test processing items with a rate limit."""
    start = time.monotonic()
    result = await async_rate_limited(echo, [1, 2, 3], max_calls=2, period=0.1)
    elapsed = time.monotonic() - start
    assert result == [1, 2, 3]
    assert elapsed >= 0.1


@pytest.mark.asyncio
async def test_async_rate_limited_tuple() -> None:
    """Test case 2: Test processing a tuple of items."""
    start = time.monotonic()
    result = await async_rate_limited(echo, (1, 2, 3), max_calls=2, period=0.1)
    elapsed = time.monotonic() - start
    assert result == [1, 2, 3]
    assert elapsed >= 0.1


@pytest.mark.asyncio
async def test_async_rate_limited_generator() -> None:
    """Test case 3: Test processing items from a generator."""
    start = time.monotonic()
    result = await async_rate_limited(echo, generate_numbers(), max_calls=2, period=0.1)
    elapsed = time.monotonic() - start
    assert result == [0, 1, 2]
    assert elapsed >= 0.1


@pytest.mark.asyncio
async def test_async_rate_limited_enforces_rate_limit() -> None:
    """Test case 4: Test that rate limit sleep is enforced when limit is reached."""

    # Use a very fast function and ensure we hit the rate limit
    async def fast_func(value: int) -> int:
        return value

    # Process 5 items with max_calls=2 and period=0.2
    # This should trigger the sleep on items 3, 4, 5
    start = time.monotonic()
    result = await async_rate_limited(
        fast_func, [1, 2, 3, 4, 5], max_calls=2, period=0.2
    )
    elapsed = time.monotonic() - start

    assert result == [1, 2, 3, 4, 5]
    # Should take at least 0.4 seconds (2 rate limit sleeps)
    assert elapsed >= 0.4


@pytest.mark.asyncio
async def test_async_rate_limited_multiple_sleeps() -> None:
    """Test case 5: Test multiple rate limit enforcements with timestamp cleanup."""

    # Test that the second while loop after sleep (line 67) is executed
    async def instant_func(value: int) -> int:
        return value

    # Process 4 items with max_calls=2 and period=0.15
    # This ensures we hit the rate limit and the cleanup loop after sleep
    start = time.monotonic()
    result = await async_rate_limited(
        instant_func, [1, 2, 3, 4], max_calls=2, period=0.15
    )
    elapsed = time.monotonic() - start

    assert result == [1, 2, 3, 4]
    # Should take at least 0.15 seconds (one sleep period minimum)
    assert elapsed >= 0.15


@pytest.mark.asyncio
async def test_async_rate_limited_invalid_params() -> None:
    """Test case 6: Test invalid parameters raise ValueError."""
    with pytest.raises(ValueError):
        await async_rate_limited(echo, [1], max_calls=0, period=0.1)
    with pytest.raises(ValueError):
        await async_rate_limited(echo, [1], max_calls=1, period=0)
