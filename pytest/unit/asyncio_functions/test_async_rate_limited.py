import asyncio
import time
import pytest
from asyncio_functions.async_rate_limited import async_rate_limited


async def echo(value: int) -> int:
    await asyncio.sleep(0.01)
    return value


@pytest.mark.asyncio
async def test_async_rate_limited_success() -> None:
    """Test processing items with a rate limit."""
    start = time.monotonic()
    result = await async_rate_limited(echo, [1, 2, 3], max_calls=2, period=1.0)
    elapsed = time.monotonic() - start
    assert result == [1, 2, 3]
    assert elapsed >= 1.0


@pytest.mark.asyncio
async def test_async_rate_limited_invalid_params() -> None:
    """Test invalid parameters raise ValueError."""
    with pytest.raises(ValueError):
        await async_rate_limited(echo, [1], max_calls=0, period=1.0)
    with pytest.raises(ValueError):
        await async_rate_limited(echo, [1], max_calls=1, period=0)
