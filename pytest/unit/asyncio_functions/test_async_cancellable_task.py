import asyncio
import pytest

from asyncio_functions.async_cancellable_task import async_cancellable_task


@pytest.mark.asyncio
async def test_async_cancellable_task_times_out_and_cancels():
    async def long_task() -> str:
        await asyncio.sleep(10)
        return "Completed"

    cancel_event = asyncio.Event()
    with pytest.raises(asyncio.CancelledError):
        await async_cancellable_task(long_task, cancel_event)

    assert cancel_event.is_set()
