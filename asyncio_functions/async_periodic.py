from typing import Callable, Awaitable
import asyncio

# Define an asynchronous function to run another function periodically
async def async_periodic(func: Callable[[], Awaitable[None]], interval: float) -> None:
    """
    Run an asynchronous function periodically with a fixed time interval.

    Parameters
    ----------
    func : Callable[[], Awaitable[None]]
        The asynchronous function to run periodically.
    interval : float
        The time interval in seconds between executions.

    Returns
    -------
    None

    Examples
    --------
    >>> async def say_hello() -> None:
    >>>     print("Hello!")
    >>> asyncio.run(async_periodic(say_hello, interval=2))
    (prints "Hello!" every 2 seconds)
    """
    # Infinite loop to run the function periodically
    while True:
        # Await the execution of the provided asynchronous function
        await func()
        # Await for the specified interval before the next execution
        await asyncio.sleep(interval)
