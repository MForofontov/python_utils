import asyncio

import pytest

from asyncio_functions.async_cancellable_task import async_cancellable_task


@pytest.mark.asyncio
async def test_async_cancellable_task_returns_result():
    """Task result is returned when cancellation is not requested."""

    cancel_event = asyncio.Event()

    async def sample_task() -> str:
        await asyncio.sleep(0.01)
        return "completed"

    result = await async_cancellable_task(sample_task, cancel_event)

    assert result == "completed"


@pytest.mark.asyncio
async def test_async_cancellable_task_cancelled_when_event_set():
    """The task is cancelled when the cancel event is triggered."""

    cancel_event = asyncio.Event()

    async def long_task() -> None:
        await asyncio.sleep(0.1)

    async def trigger_cancel() -> None:
        await asyncio.sleep(0.01)
        cancel_event.set()

    cancel_trigger = asyncio.create_task(trigger_cancel())

    with pytest.raises(asyncio.CancelledError):
        await async_cancellable_task(long_task, cancel_event)

    await cancel_trigger


@pytest.mark.asyncio
async def test_async_cancellable_task_timeout():
    """A timeout raises asyncio.TimeoutError when reached first."""

    cancel_event = asyncio.Event()

    async def long_task() -> None:
        await asyncio.sleep(0.1)

    with pytest.raises(asyncio.TimeoutError):
        await async_cancellable_task(long_task, cancel_event, timeout=0.01)
