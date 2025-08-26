import asyncio
import time
import pytest
from asyncio_functions.async_rate_limited import async_rate_limited


async def echo(value: int) -> int:
    await asyncio.sleep(0.01)
    return value


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


def generate_numbers():
    for i in range(3):
        yield i


@pytest.mark.asyncio
async def test_async_rate_limited_generator() -> None:
    """Test case 3: Test processing items from a generator."""
    start = time.monotonic()
    result = await async_rate_limited(echo, generate_numbers(), max_calls=2, period=0.1)
    elapsed = time.monotonic() - start
    assert result == [0, 1, 2]
    assert elapsed >= 0.1


@pytest.mark.asyncio
async def test_async_rate_limited_invalid_params() -> None:
    """Test case 4: Test invalid parameters raise ValueError."""
    with pytest.raises(ValueError):
        await async_rate_limited(echo, [1], max_calls=0, period=0.1)
    with pytest.raises(ValueError):
        await async_rate_limited(echo, [1], max_calls=1, period=0)
