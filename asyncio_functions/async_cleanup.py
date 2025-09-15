from typing import TypeVar
from collections.abc import Callable
from collections.abc import Awaitable

# Define a type variable T to represent the return type of the main task
T = TypeVar("T")


async def async_cleanup(
    func: Callable[[], Awaitable[T]], cleanup: Callable[[], Awaitable[None]]
) -> T:
    """
    Ensure proper cleanup after an asynchronous task, even if it fails.

    Parameters
    ----------
    func : Callable[[], Awaitable[T]]
        The main asynchronous task to run.
    cleanup : Callable[[], Awaitable[None]]
        The cleanup function to run after the task, regardless of success or failure.

    Returns
    -------
    T
        The result of the main task.

    Examples
    --------
    >>> async def risky_task() -> str:
    >>>     await asyncio.sleep(1)
    >>>     raise ValueError("An error occurred")
    >>>
    >>> async def close_resources() -> None:
    >>>     print("Resources cleaned up")
    >>>
    >>> try:
    >>>     result = asyncio.run(async_cleanup(risky_task, close_resources))
    >>> except Exception as e:
    >>>     print(e)
    >>> finally:
    >>>     print("Cleanup ensured")
    Resources cleaned up
    Cleanup ensured
    ValueError: An error occurred
    """
    try:
        # Await the execution of the main asynchronous task
        return await func()
    finally:
        # Ensure the cleanup function is called, regardless of success or failure
        await cleanup()


__all__ = ["async_cleanup"]
