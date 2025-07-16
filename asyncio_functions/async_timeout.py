from typing import TypeVar, Awaitable
from collections.abc import Callable
import asyncio

# Define a type variable T to represent the return type of the function
T = TypeVar('T')

async def async_timeout(func: Callable[..., Awaitable[T]], timeout: float) -> T:
    """
    Add a timeout to an asynchronous function.

    Parameters
    ----------
    func : Callable[..., Awaitable[T]]
        The asynchronous function to run.
    timeout : float
        The time in seconds after which to timeout the function.

    Returns
    -------
    T
        The result of the function if successful.

    Raises
    ------
    asyncio.TimeoutError
        If the function does not complete within the specified timeout.

    Examples
    --------
    >>> async def long_task() -> str:
    >>>     await asyncio.sleep(10)
    >>>     return "Finished"
    >>> asyncio.run(async_timeout(long_task, timeout=5))
    asyncio.TimeoutError: Task did not finish in 5 seconds
    """
    return await asyncio.wait_for(func(), timeout)
