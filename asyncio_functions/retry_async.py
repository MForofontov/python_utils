from typing import TypeVar, Awaitable
from collections.abc import Callable
import asyncio

# Define a type variable for the return type of the function
T = TypeVar("T")


async def retry_async(
    func: Callable[..., Awaitable[T]],
    retries: int,
    delay: float,
) -> T:
    """
    Retry an asynchronous function a specified number of times if it fails.

    Parameters
    ----------
    func : Callable[..., Awaitable[T]]
        The asynchronous function to retry.
    retries : int
        The maximum number of retry attempts.
    delay : float
        The delay in seconds between retry attempts.

    Returns
    -------
    T
        The result of the function if successful.

    Raises
    ------
    Exception
        If the function fails after all retries.

    Examples
    --------
    >>> async def unstable_func() -> int:
    >>>     if random.random() < 0.5:
    >>>         raise ValueError("Failed!")
    >>>     return 42
    >>> asyncio.run(retry_async(unstable_func, retries=3, delay=1))
    42
    """
    for attempt in range(retries):
        try:
            return await func()
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise e

__all__ = ['retry_async']
