import asyncio
from typing import TypeVar
from collections.abc import Callable
from collections.abc import Awaitable

# Define a type variable T to represent the return type of the function
T = TypeVar("T")


def async_event_loop(func: Callable[[], Awaitable[T]]) -> T:
    """
    Create and run an asynchronous event loop for testing.

    Parameters
    ----------
    func : Callable[[], Awaitable[T]]
        The asynchronous function to run in the event loop.

    Returns
    -------
    T
        The result of the asynchronous function.

    Examples
    --------
    >>> async def test_function() -> str:
    >>>     await asyncio.sleep(1)
    >>>     return "Test completed"
    >>>
    >>> result = async_event_loop(test_function)
    >>> print(result)  # Output: "Test completed"
    """

    async def wrapper() -> T:
        return await func()

    # Run the provided asynchronous function in an event loop and return the result
    return asyncio.run(wrapper())
