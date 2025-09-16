import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

# Define a type variable T to represent the return type of the function
T = TypeVar("T")


def async_event_loop(func: Callable[[], Awaitable[T]]) -> T:
    """
    Create and run an asynchronous event loop for testing.

    By default, the provided asynchronous function is executed using
    :func:`asyncio.run`. If this function is invoked while an event loop is
    already running (for example, inside a Jupyter notebook), ``asyncio.run``
    raises a ``RuntimeError``. In that case a new event loop is created and the
    coroutine is executed with ``loop.run_until_complete`` before the loop is
    closed.

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
    try:
        return asyncio.run(wrapper())
    except RuntimeError as exc:
        if "asyncio.run() cannot be called from a running event loop" not in str(exc):
            raise
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(wrapper())
        finally:
            loop.close()


__all__ = ["async_event_loop"]
