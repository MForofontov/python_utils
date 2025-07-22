import asyncio
from typing import TypeVar, Awaitable
from collections.abc import Callable

# Define a type variable T to represent the return type of the function
T = TypeVar('T')

async def async_retry_with_backoff(
    func: Callable[..., Awaitable[T]],
    retries: int,
    initial_delay: float,
    backoff_factor: float,
) -> T:
    """
    Retry an asynchronous function on failure, using exponential backoff.

    Parameters
    ----------
    func : Callable[..., Awaitable[T]]
        The asynchronous function to retry.
    retries : int
        The maximum number of retry attempts.
    initial_delay : float
        The initial delay in seconds before the first retry.
    backoff_factor : float
        The factor by which the delay is multiplied after each retry.

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
    >>> async def sometimes_fails() -> int:
    >>>     if random.random() < 0.5:
    >>>         raise ValueError("Random failure")
    >>>     return 42
    >>> asyncio.run(async_retry_with_backoff(sometimes_fails, retries=5, initial_delay=1, backoff_factor=2))
    42
    """
    # Initialize the delay with the initial delay value
    delay = initial_delay
    
    # Loop through the number of retries
    for attempt in range(retries):
        try:
            # Try to execute the asynchronous function
            return await func()
        except Exception as e:
            # If an exception occurs and retries are left
            if attempt < retries - 1:
                # Wait for the current delay duration
                await asyncio.sleep(delay)
                # Increase the delay by the backoff factor
                delay *= backoff_factor
            else:
                # If no retries are left, raise the exception
                raise e
